# Persona 
*A local, private AI-powered interview coach.*  

---

Jump to [Overview](#overview)  
Jump to [Why GPT-OSS:20B](#why-gpt-oss20b)  
Jump to [Project Structure](#project-structure)  
Jump to [Requirements](#requirements)  
Jump to [Install dependencies](#install-dependencies)  
Jump to [Important Ollama Setup](#ollama-setup)  
Jump to [Usage](#usage)  
Jump to [Tech Stack](#tech-stack)  
Jump to [License](#license)  
Jump to [Author](#author)

Try it out [Windows Executable](#get-persona)

---

Live walktrough 👉 [Youtube](https://youtu.be/p3zfJGWsXyQ)

## Overview  
**Persona** is a completely **local AI interview coach** that helps candidates practice for interviews across any domain.  

Unlike online tools, Persona ensures **100% privacy** by running fully on your machine. It adapts to your skills, the employer’s requirements, and provides **real-time verbal interviews** powered by the **GPT-OSS:20B** model.  

Persona also uses **Mediapipe + OpenCV** to analyze your **posture and body language** during the session, giving instant feedback and generating detailed reports with:  
- 📊 Confidence scoring  
- 🗣️ Answer quality  
- 🌐 English proficiency  
- 🧍 Posture tracking  
- 📑 Recruiter insights  

Built with **Flet**, Persona delivers a **sleek, minimalist GUI** optimized for performance so that system resources are prioritized for the model itself.  

---

## Why GPT-OSS:20B?  
Persona is powered by **GPT-OSS:20B**, chosen specifically for its unique advantages:  

- 📏 **128K context window** → handles long interviews seamlessly.  
- ⚡ **MXFP4 quantization** → reduces memory + compute requirements while maintaining high accuracy.  
- 🔀 **Mixture-of-Experts architecture** → enables blazing-fast inference speeds, even on CPU. 

This combination makes Persona **fast, private, and reliable** — unlike most online interview tools.  

---


## Screenshots  

![Landing Page](Persona%20demo/Screenshot%202025-09-02%20115239.png)  
*Minimalist landing page with "Get Started" flow.*  

![Interview Session](Persona%20demo/Screenshot%202025-09-09%20154458.png)
*Live posture tracking and verbal interview interface.*  

![Analytics Report](Persona%20demo/Screenshot%202025-09-09%20154348.png)  
*Line graph showing confidence, answer quality, proficiency, and posture.*  

---

## Project Structure  

```bash
Persona/              
├── 08-09, 19-34.json       # Session/experiment logs
├── 08-09, 19-44.json
├── 08-09, 20-48.json
├── 08-09, 22-34.json
│
├── LICENSE                 # License file
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
│
├── Sylphie_voice.py        # Voice synthesis and processing (Piper TTS)
├── eye_detection.py        # Eye detection / vision-based module
├── hugginface_inference.py # Hugging Face inference integration
├── main.py                 # Main entry point of the project
├── ollama_gpt.py           # Ollama GPT integration module (GPT-OSS:20B)
├── python_pdf_docx.py      # PDF/Docx processing module (CV parsing)
│
├── assets/                 
│   ├── fonts/              # Montserrat-Regular.ttf 
│   └── images/             # App icons, graphics, screenshots
│
├── piper_models/           # Voice models (Piper TTS, default voice included as hfc_female)
└── .gitignore
```

## Requirements

- Python 3.12.7
- Ollama (for GPT-OSS:20B local inference)
- CUDA-compatible GPU (optional, for faster inference)
- Works on Linux / macOS / Windows
- At least 16gb of system RAM

## Install dependencies

```
git clone https://github.com/<your-username>/persona.git
cd persona
python3.12 -m venv venv
source venv/bin/activate   # (or venv\Scripts\activate on Windows)
pip install -r requirements.txt
```
## Ollama Setup

> 🔴 Note: Persona relies on GPT-OSS:20B running locally via Ollama. Make sure you have the correct Ollama version installed and running.

Install Ollama → [Download here](https://ollama.com/download)

Verify Ollama version

```
ollama --version
```
(Recommended: latest stable version)

Pull GPT-OSS:20B model
```
ollama pull gpt-oss:20b
```

Start Ollama service (must run in the background)
```
ollama run gpt-oss:20b
```

## Usage

Start the app
```
python main.py
```

On launch:
- Click Get Started.

- Upload your CV (PDF/DOCX) or skip for demo.

- Choose your field of work and role.

- Enter details about yourself and what the employer is looking for.

- Persona begins the mock interview:

- Verbal Q/A in real time with GPT-OSS:20B.

- Faster-Whisper handles speech-to-text.

- Posture analysis runs with Mediapipe + OpenCV.

> After interview:

Get detailed analytics with graphs and recruiter-style notes.

## Get Persona

**💾 Download the fully compiled Windows version of Persona here:**

[⬇️ Download Persona (.exe)](https://drive.google.com/file/d/1SVWAxLc-BGjMz_MPT3OJru-wEnplE19_/view?usp=sharing)

> ⚠️ Note: Make sure you have **at least 16 GB RAM** and Ollama installed for GPT-OSS:20B and active.


## Tech Stack

- LLM: GPT-OSS:20B (via Ollama)
- Runner: Ollama (local model hosting)
- STT: Faster-Whisper (small model, GPU-accelerated if available)
- TTS: Piper (default female voice hfc_female)
- GUI: Flet
- Vision: Mediapipe + OpenCV (posture, eye detection)
- Python: 3.12.7

## License 
Apache 2.0

## Author
Developed by Anshul.





