import cv2
import mediapipe as mp
import numpy as np
import time
from flask import Flask, Response, send_file
import threading
import os
from flask import jsonify, request



CAMERA_INDEX = 1
PORT = 5000 
CHEST_POINT_RATIO = 0.25
CALIBRATE_SECONDS = 3.0
CHEST_SLOUCH_THRESHOLD_DEG = 12.0
FORWARDNESS_THRESHOLD = 0.15
SMOOTHING_ALPHA = 0.6
STATE_STABILITY_FRAMES = 5

running=True


mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6)


good_count, bad_count, lost_count = 0, 0, 0
last_state, stable_frames = None, 0
baseline = 0
smoothed_angle, smoothed_forward = None, None


latest_frame = None
lock = threading.Lock()


def midpoint(a, b): 
    return (a + b) / 2.0


def vector_angle_deg(v, w):
    v, w = np.array(v, float), np.array(w, float)
    nv, nw = np.linalg.norm(v), np.linalg.norm(w)
    if nv == 0 or nw == 0:
        return 0.0
    cosang = np.dot(v, w) / (nv * nw)
    cosang = np.clip(cosang, -1.0, 1.0)
    return float(np.degrees(np.arccos(cosang)))


def compute_chest_metrics(landmarks, shape):
    ih, iw = shape
    def lm_point(lm): return np.array([lm.x * iw, lm.y * ih])
    try:
        l_sh = lm_point(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value])
        r_sh = lm_point(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value])
        l_hi = lm_point(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])
        r_hi = lm_point(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value])
        nose = lm_point(landmarks[mp_pose.PoseLandmark.NOSE.value])
    except Exception:
        return None
    shoulder_mid = midpoint(l_sh, r_sh)
    hip_mid = midpoint(l_hi, r_hi)
    chest_point = shoulder_mid + CHEST_POINT_RATIO * (hip_mid - shoulder_mid)
    upper_vec = nose - chest_point
    vertical = np.array([0.0, 1.0])
    angle_deg = vector_angle_deg(upper_vec, vertical)
    forwardness = float(upper_vec[0] / (np.linalg.norm(upper_vec) + 1e-6))
    return {
        "chest_point": chest_point,
        "nose": nose,
        "angle_deg": angle_deg,
        "forwardness": forwardness
    }


def calibrate(cap):
    calib_vals, start = [], time.time()
    while time.time() - start < CALIBRATE_SECONDS:
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.flip(frame, 1)
        res = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if res.pose_landmarks:
            m = compute_chest_metrics(res.pose_landmarks.landmark, frame.shape[:2])
            if m:
                calib_vals.append(m["angle_deg"])
    return np.median(calib_vals) if calib_vals else 0



def frame_grabber():
    global good_count, bad_count, lost_count, last_state, stable_frames
    global smoothed_angle, smoothed_forward, baseline, latest_frame
    global running

    cap = cv2.VideoCapture(CAMERA_INDEX)
    baseline = calibrate(cap)
    print(f"Calibration done. Baseline = {baseline:.2f} deg")

    while running:
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.flip(frame, 1)
        res = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        current_state, confidence = "Lost", "No"
        if res.pose_landmarks:
            m = compute_chest_metrics(res.pose_landmarks.landmark, frame.shape[:2])
            if m:
                confidence = "Yes"
                angle, fwd = m["angle_deg"], m["forwardness"]
                if smoothed_angle is None:
                    smoothed_angle, smoothed_forward = angle, fwd
                else:
                    smoothed_angle = SMOOTHING_ALPHA * angle + (1 - SMOOTHING_ALPHA) * smoothed_angle
                    smoothed_forward = SMOOTHING_ALPHA * fwd + (1 - SMOOTHING_ALPHA) * smoothed_forward
                angle_adj = smoothed_angle - baseline
                current_state = "Bad" if (
                    angle_adj > CHEST_SLOUCH_THRESHOLD_DEG or abs(smoothed_forward) > FORWARDNESS_THRESHOLD
                ) else "Good"
                cp = tuple(m["chest_point"].astype(int))
                cv2.circle(frame, cp, 6, (255, 0, 0), -1)

        
        
        
            
            if current_state == "Good":
                good_count += 1
            elif current_state == "Bad":
                bad_count += 1
            elif current_state == "Lost":
                lost_count += 1
            

     
        
        cv2.putText(frame, f"Posture: {current_state}", (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 0, 255) if current_state == "Bad" else (0, 200, 0), 2)
        

        
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        
        with lock:
            latest_frame = buffer.tobytes()
    cap.release()
    cv2.destroyAllWindows()

 
app = Flask(__name__)


@app.route('/frame.jpg')
def frame_jpg():
    global latest_frame
    with lock:
        if latest_frame is None:
            return "No frame yet", 503
        return Response(latest_frame, mimetype='image/jpeg')


@app.route('/video_feed')
def video_feed():
    def gen():
        while True:
            with lock:
                if latest_frame is None:
                    continue
                frame_bytes = latest_frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(0.05)  # ~20 FPS
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


from flask import after_this_request

@app.route('/stop')
def stop():
    global running
    running = False

    stats = {
        "good_count": good_count,
        "bad_count": bad_count,
        "lost_count": lost_count
    }

    @after_this_request
    def shutdown(response):
        shutdown_func = request.environ.get('werkzeug.server.shutdown')
        if shutdown_func:
            shutdown_func()
        return response

    return jsonify(stats)




def run():
    threading.Thread(target=frame_grabber, daemon=True).start()
    print(f"Serving on http://127.0.0.1:{PORT}/frame.jpg and /video_feed")
    app.run(host="0.0.0.0", port=PORT, debug=False, threaded=True)

