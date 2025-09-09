import numpy as np
import sounddevice as sd

from piper.voice import PiperVoice



model_path = "piper_models/en_US-hfc_female-medium.onnx"
config_path = "piper_models/en_US-hfc_female-medium.onnx.json"


voice = PiperVoice.load(model_path, config_path=config_path, use_cuda=True)

def fade_out(audio_data, fade_duration=0.2, samplerate=22050):
    fade_samples = int(fade_duration * samplerate)
    if fade_samples > len(audio_data):
        fade_samples = len(audio_data)
    fade_curve = np.linspace(1, 0, fade_samples)
    audio_data[-fade_samples:] = (audio_data[-fade_samples:] * fade_curve).astype(np.int16)
    return audio_data


def speak_streaming(text):
    final_audio = []
    for chunk in voice.synthesize(text):
        audio_data = np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16)
        final_audio.append(audio_data)
    final_audio = np.concatenate(final_audio)
    final_audio = fade_out(final_audio, fade_duration=0.2, samplerate=chunk.sample_rate)

    sd.play(final_audio, samplerate=chunk.sample_rate)
    sd.wait()
        

# if __name__ == "__main__":
#     #while True:
#     #string=input("enter")
            
#     speak_streaming("You mentioned that Suryen uses a multi‑threaded, event‑driven architecture to keep the UI responsive. How would you handle thread‑safety when updating the UI from background threads (e.g., in a Win32/GTK/Flet environment)?")