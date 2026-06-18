# 🎙️ VoiceGuard — Multilingual AI Voice Deepfake Detector

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-CNN-red?style=flat-square&logo=pytorch)
![Flask](https://img.shields.io/badge/Flask-Web%20App-black?style=flat-square&logo=flask)
![Accuracy](https://img.shields.io/badge/Test%20Accuracy-95%25-brightgreen?style=flat-square)
![Languages](https://img.shields.io/badge/Languages-5-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

> A CNN-based voice deepfake detection system that identifies AI-generated speech across **5 languages** — English, Hindi, Kannada, Marathi, and Telugu — with **95% test accuracy** and **100% fake-detection precision**. Runs entirely on CPU, no GPU required.

---

## 📌 Overview

Voice cloning tools like ElevenLabs and Tortoise-TTS can now synthesize convincing fake audio from just seconds of real speech. Most existing detection systems only support English, leaving hundreds of millions of Indian-language speakers unprotected.

**VoiceGuard** fills this gap. It extracts MFCC (Mel-Frequency Cepstral Coefficient) features from audio and feeds them into a lightweight 2D CNN classifier to distinguish real human speech from AI-generated audio — in real time, via microphone or file upload.

---

## ✨ Features

- 🌐 **Multilingual** — English, Hindi, Kannada, Marathi, Telugu
- 🧠 **CNN on MFCC** — treats audio features as 2D images for classification
- ⚡ **CPU-only** — no GPU required, runs on a regular laptop
- 🎙️ **Real-time detection** — live microphone recording support
- 📂 **File upload** — supports WAV, MP3, M4A, OGG, FLAC, WebM
- 🌊 **Silence detection** — rejects empty/noise-only recordings
- ⚠️ **Language warning** — alerts when unsupported language is used
- 🖥️ **Flask web app** — clean dark-themed UI with confidence scores

---

## 🏗️ System Architecture

```
Audio Input (Mic / File)
        ↓
  Preprocess: 16kHz, mono, 3s, normalize
        ↓
  MFCC Extraction: 40×301 feature matrix
        ↓
  VoiceCNN (3-block CNN classifier)
        ↓
  Output: REAL / FAKE + Confidence %
```

---

## 🧠 Model Architecture — VoiceCNN

| Layer | Details |
|---|---|
| Conv Block 1 | Conv2d(1→32) + BN + ReLU + MaxPool + Dropout(0.2) |
| Conv Block 2 | Conv2d(32→64) + BN + ReLU + MaxPool + Dropout(0.2) |
| Conv Block 3 | Conv2d(64→128) + BN + ReLU + AdaptiveAvgPool(4×4) |
| FC Layers | Linear(2048→256) → Linear(256→64) → Linear(64→2) |
| Total Params | 634,242 |

---

## 📊 Results

| Metric | Value |
|---|---|
| Test Accuracy | **95%** |
| Fake Precision | **100%** |
| Fake Recall | 90% |
| Real Precision | 91% |
| Real Recall | 100% |
| Training Epochs | 25 |
| Dataset Size | 412 samples (balanced) |

### Comparison with other approaches

| Model | Accuracy | GPU Needed | Multilingual |
|---|---|---|---|
| AASIST | ~99%* | ✅ Yes | ❌ No |
| RawNet2 | ~97%* | ✅ Yes | ❌ No |
| SVM + MFCC | ~78% | ❌ No | Limited |
| **VoiceCNN (ours)** | **95%** | **❌ No** | **✅ Yes (5 langs)** |

*On ASVspoof 2019 benchmark (different, larger dataset)

---

## 🗃️ Dataset

| Source | Language | Type | Samples |
|---|---|---|---|
| DEEP-VOICE (Kaggle) | English | Real celebrity | 8 |
| DEEP-VOICE fake (Kaggle) | English | Voice converted | 56 |
| Indian Languages Audio Dataset (Kaggle) | Hindi/Kn/Mr/Te | Real human | 198 |
| gTTS generated | All 5 langs | AI synthesised | ~150 |

Dataset was balanced to 206 samples per class with 80/10/10 stratified split.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- ffmpeg (required for microphone WebM recordings)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/voiceguard.git
cd voiceguard

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install ffmpeg (Windows)
# Download from https://ffmpeg.org/download.html and add bin/ to PATH
```

### Run

```bash
python app.py
# Open http://localhost:5000
```

---

## 📦 Requirements

```
flask
numpy
torch
librosa
soundfile
```

> Create `requirements.txt` with `pip freeze > requirements.txt`

---

## 📁 Project Structure

```
voiceguard/
├── app.py                  # Flask backend + prediction pipeline
├── voice_detector.pt       # Trained model weights
├── templates/
│   └── index.html          # Frontend web app
├── static/
│   ├── samples/            # Sample audio files
│   └── graphs/             # Training curves, confusion matrix
└── requirements.txt
```

---

## ⚠️ Known Limitations

- Struggles to detect **modern neural voice cloning** tools like ElevenLabs or RVC, which produce highly natural speech with minimal spectral artifacts
- Training dataset is relatively small (412 samples) compared to large benchmarks like ASVspoof 2019 (100,000+ utterances)

---

## 🔮 Future Work

- Add ElevenLabs and RVC cloned voice samples to training data
- Explore Wav2Vec2 pre-trained embeddings for richer feature representation
- Expand language support to Bengali, Tamil, Gujarati, Punjabi
- Deploy with TensorFlow Lite for mobile/edge devices

---

## 👥 Authors

**Shrusti Miskin** 
Department of Cyber Security, AI Computer Science
Dayananda Sagar University, Bengaluru, India

---

## 📄 References

1. Wu et al., "ASVspoof," IEEE J. Sel. Topics Signal Process., 2017
2. Tak et al., "End-to-end anti-spoofing with RawNet2," ICASSP 2021
3. Jung et al., "AASIST," ICASSP 2022
4. DEEP-VOICE Dataset — [Kaggle](https://www.kaggle.com/datasets/birdy654/deep-voice-deepfake-voice-recognition)
5. Indian Languages Audio Dataset — [Kaggle](https://www.kaggle.com/datasets/hmsolanki/indian-languages-audio-dataset)

---

## 📜 License

This project is licensed under the MIT License.
