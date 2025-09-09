import threading
import queue
import json
from ollama import Client
import Sylphie_voice
import flet as ft
import webrtcvad
from faster_whisper import WhisperModel
import pyaudio
import queue
import numpy as np





class GPTInterview:
    def __init__(self, user_info, job_role, interview_type, no_of_questions, interview_req, file_name ):
        self.filename=file_name
        self.messages = [
            {
                "role": "system",
                "content": (
                    "You are a professional job interviewer speaking with the candidate. "
                    "Your main goal is to evaluate the candidate’s suitability for the role while making the conversation feel natural, "
                    "engaging, and respectful — just like a real human interviewer. "
                    f"You should ask up to {no_of_questions} thoughtful questions based on the candidate’s background. "
                    f"The candidate’s skills are: {user_info}. "
                    f"The job role is {job_role}, with key requirements: {interview_req}. "
                    f"Conduct the interview in a {interview_type} style. "
                    "If the candidate asks you something, you may respond conversationally (brief, natural replies) "
                    "before continuing the interview flow. "
                    "Avoid robotic phrasing — keep your wording warm, human-like, and adaptive."
                ),
            },
            {
                "role": "system",
                "content": (
                    "Your reply must ALWAYS be in a single JSON object (no Markdown, no text outside JSON). "
                    "Never repeat the same object twice. Never output arrays unless explicitly asked. "
                    "Use exactly this schema:\n\n"
                    "{\n"
                    '  "question_number": <integer>,\n'
                    '  "type": "<General | Programming | Behavioral | Technical | DSA>",\n'
                    '  "text": "<the next interview question or conversational reply, phrased naturally>",\n'
                    '  "evaluation": {\n'
                    '    "english_proficiency": <0-10 or null>,\n'
                    '    "confidence": <0-10 or null>,\n'
                    '    "content_quality": <0-10 or null>,\n'
                    '    "notes": "<short natural note about the candidate’s last answer, or empty if no answer yet>"\n'
                    "  },\n"
                    '  "end": <true | false>\n'
                    "}\n\n"
                    "Evaluation rules:\n"
                    "- If this is the very first question (no answer yet), leave all evaluation fields null.\n"
                    "- Otherwise, score english_proficiency (clarity & grammar), confidence (assurance & fluency), and content_quality (depth & relevance) on 1–10.\n"
                    "- notes should be short and natural, like an interviewer jotting impressions (not robotic)."
                ),
            },
            {
                "role": "system",
                "content": (
                    "Question rules:\n"
                    "- Always choose exactly one type.\n"
                    "- 'General' for introductions, background, and motivation.\n"
                    "- 'Behavioral' for teamwork, conflict resolution, and soft skills.\n"
                    "- 'Technical' for system design, architecture, applied technology.\n"
                    "- 'Programming' for language-specific or conceptual discussions (without requiring code).\n"
                    "- 'DSA' only when asking the candidate to explain/write an algorithm or implementation.\n"
                    "You may also give short conversational replies to candidate’s questions or comments — keep them warm and professional, "
                    "then smoothly continue with the interview."
                ),
            },
            {
                "role": "system",
                "content": (
                    "Start with: question_number=1, type='General', asking the candidate to introduce themselves in a friendly, natural way."
                ),
            },
        ]

        

        




        self.client = Client()
        self.model = "gpt-oss:20b"
        
        self.speech_q = queue.Queue()
        self.speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.speech_thread.start()

    def _speech_worker(self):
        """Thread worker to handle speaking sentences in sequence."""
        while True:
            sentence = self.speech_q.get()
            if sentence is None:
                break
            Sylphie_voice.speak_streaming(sentence + "   ...")
            self.speech_q.task_done()

    def chat_with_model(self, user_input: str, container: ft.Container, text: ft.Text, mic: ft.Container, current_theme, current_text_theme):
        self.messages.append({"role": "user", "content": user_input})

        stream = self.client.chat(
            model=self.model,
            messages=self.messages,
            stream=True,
            think='low',
            options={"num_predict": 500}
        )

        print("\n--- Streaming Response ---\n")

        buffer = ""       
        voice_buffer = "" 
        brace_count = 0   
        inside_json = False
        full_response = ""

        container.content = ft.Column(
            [ft.Row([text], alignment=ft.MainAxisAlignment.CENTER, wrap=True)],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            scroll="auto"
        )


        capturing_question = False
        looking_for_question = False
        question_buffer = ""
        key_buffer = ""
        parsed={}
        
        print("Storing in",self.filename)
        
        with open(self.filename, "a") as f:
            try:
                for chunk in stream:
                    content = chunk["message"]["content"]
                    full_response += content

                    for char in content:
                        if char == "{":
                            brace_count += 1
                            inside_json = True
                        if inside_json:
                            buffer += char

                        
                        if not capturing_question:
                            key_buffer += char
                            if key_buffer.endswith('"text":"'):
                                capturing_question = True
                                question_buffer = ""
                                key_buffer = ""
                        else:
                            if char in ['"', '}']:
                                
                                capturing_question = False
                                text.value = question_buffer
                                container.update()
                                print("[Captured Question]:", question_buffer)

                               
                                voice_buffer += question_buffer
                                while '.' in voice_buffer:
                                    sentence, remainder = voice_buffer.split('.', 1)
                                    sentence += '.'
                                    self.speech_q.put(sentence.strip())
                                    voice_buffer = remainder

                                question_buffer = ""
                            else:
                                
                                question_buffer += char
                                text.value = question_buffer
                                container.update()

                        if char == "}":
                            brace_count -= 1
                            if brace_count == 0 and inside_json:
                                try:
                                    parsed = json.loads(buffer)
                                    json.dump(parsed, f, indent=4)
                                    f.write(",\n")
                                except json.JSONDecodeError as e:
                                    print("JSON parse error:", e, buffer)
                                buffer = ""
                                inside_json = False

            except Exception as e:
                print("Error:", e)

        if voice_buffer.strip():
            self.speech_q.put(voice_buffer.strip())

        self.messages.append({"role": "assistant", "content": full_response})
        print("\n--- End of Response ---\n")
        print("Parsed",parsed)
        if not parsed.get("end", True):
            mic.content = ft.Column([
                ft.IconButton(
                    icon=ft.Icons.MIC_SHARP,
                    icon_color=current_text_theme,
                    hover_color=current_theme,
                    icon_size=50
                ),
                ft.Text("Listening...")
            ], alignment=ft.MainAxisAlignment.CENTER)
            mic.update()
            speech = SimpleSTT().run()
            mic.content = ft.Column([ft.Text(speech, size=27)], scroll="auto")
            

            
            mic.update()
            

            return self.chat_with_model(speech, container, text, mic, current_theme, current_text_theme)
        if parsed=={}:
            self.chat_with_model("", container, text, mic, current_theme, current_text_theme)
        
        


class SimpleSTT:
    def __init__(self, model_size="small"):
        print(f"Loading Whisper model: {model_size}")
        self.model = WhisperModel(f"{model_size}.en", device="cuda", compute_type="float16")

        self.RATE = 16000
        self.CHUNK = 320
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1

        self.vad = webrtcvad.Vad(3)

        self.audio_queue = queue.Queue()
        self.is_recording = False
        self.triggered = False
        self.voiced_frames = []
        self.silence_count = 0
        self.silence_threshold = 30

        self.audio = pyaudio.PyAudio()
        print("🎤 Ready - speak to start transcription")

    def audio_callback(self, in_data, frame_count, time_info, status):
        if self.is_recording:
            self.audio_queue.put(in_data)
        return (in_data, pyaudio.paContinue)

    def is_speech(self, frame):
        try:
            return self.vad.is_speech(frame, self.RATE)
        except:
            return False

    def transcribe(self, audio_data):
        try:
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            segments, _ = self.model.transcribe(audio_np, language="en")
            return " ".join([seg.text for seg in segments]).strip()
        except Exception as e:
            print(f"Error: {e}")
            return ""

    def run(self):
        self.is_recording = True
        stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            stream_callback=self.audio_callback
        )
        stream.start_stream()

        print("🎤 Ready - start speaking")

        silence_frames = 0

        try:
            while self.is_recording:
                try:
                    frame = self.audio_queue.get(timeout=0.1)
                    speech_detected = self.is_speech(frame)

                    if not self.triggered:
                        
                        if speech_detected:
                            print("🗣️ Speech detected")
                            self.triggered = True
                            self.voiced_frames = [frame]
                            silence_frames = 0
                    else:
                        self.voiced_frames.append(frame)

                        if speech_detected:
                            silence_frames = 0 
                        else:
                            silence_frames += 1
                            if silence_frames >= 100:  
                                print("🔇 Long pause detected - processing...")
                                audio_data = b''.join(self.voiced_frames)
                                text = self.transcribe(audio_data)
                                print(f"📝 {text}")

                                self.triggered = False
                                self.voiced_frames = []
                                silence_frames = 0
                                return text

                except queue.Empty:
                    continue
                except KeyboardInterrupt:
                    break
        finally:
            stream.stop_stream()
            stream.close()
            self.audio.terminate()


# if __name__ == "__main__":
#     interview = GPTInterview(
#         user_info="skilled in ai/ml",
#         job_role="software development",
#         interview_type="friendly",
#         no_of_questions=20,
#         interview_req="SDE 2",
#         container=ft.Container()
#     )

#     while True:
#         user_text = input("You: ")
#         interview.chat_with_model(user_text)
