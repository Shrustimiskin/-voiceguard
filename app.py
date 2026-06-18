"""
app.py — Voice Deepfake Detection Web App (Fixed Version)
Fixes:
  1. Silence / no-speech detected as REAL → now returns ERROR
  2. Language mismatch warning added
Run: python app.py  →  open http://localhost:5000
"""

import os, json, tempfile, base64
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
import numpy as np
import torch
import torch.nn as nn
import librosa

app = Flask(__name__)

# ── CONFIG ────────────────────────────────────────────────────
SR       = 16000
DURATION = 3
N_MFCC   = 40
MAX_LEN  = SR * DURATION          # 48000 samples
MPATH    = 'voice_detector.pt'
DEVICE   = torch.device('cpu')

SAMPLES_DIR = r'D:\AICS PROJECT\static\samples'

# Minimum RMS energy to consider audio as "has speech"
# Audio below this threshold is considered silence/noise
SILENCE_THRESHOLD = 0.005

# Languages the model was trained on
SUPPORTED_LANGUAGES = {'en', 'hi', 'kn', 'mr', 'te'}

# ── MODEL ─────────────────────────────────────────────────────
class VoiceCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1), nn.BatchNorm2d(32),
            nn.ReLU(), nn.MaxPool2d(2), nn.Dropout2d(0.2),
            nn.Conv2d(32, 64, 3, padding=1), nn.BatchNorm2d(64),
            nn.ReLU(), nn.MaxPool2d(2), nn.Dropout2d(0.2),
            nn.Conv2d(64, 128, 3, padding=1), nn.BatchNorm2d(128),
            nn.ReLU(), nn.AdaptiveAvgPool2d((4, 4)),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 4 * 4, 256), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(256, 64),          nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(64, 2)
        )
    def forward(self, x):
        return self.classifier(self.features(x))

model = VoiceCNN().to(DEVICE)
if Path(MPATH).exists():
    ckpt = torch.load(MPATH, map_location=DEVICE)
    model.load_state_dict(ckpt['model_state_dict'])
    model.eval()
    print(f'✅ Model loaded — val_acc={ckpt["val_acc"]:.4f}')
else:
    print(f'⚠️  Model file not found: {MPATH}')

# ── SILENCE DETECTOR ──────────────────────────────────────────
def is_silent(y, threshold=SILENCE_THRESHOLD):
    """
    Returns True if the audio is too quiet to contain speech.
    Uses RMS (Root Mean Square) energy.
    """
    rms = np.sqrt(np.mean(y ** 2))
    return rms < threshold

# ── PREDICTION FUNCTION ───────────────────────────────────────
def predict(audio_path, lang=None):
    """
    Load audio, check for silence, extract MFCC, run model.
    Returns dict with label, confidence, probabilities, and any warnings.
    """
    try:
        # Load audio
        y, _ = librosa.load(audio_path, sr=SR, mono=True, duration=DURATION)

        # ── FIX 1: Silence check ──────────────────────────────
        if is_silent(y):
            return {
                'error': 'No speech detected. Please speak clearly into the microphone and try again.',
                'error_type': 'silence'
            }

        # Pad or trim
        if len(y) < MAX_LEN:
            y = np.pad(y, (0, MAX_LEN - len(y)))
        else:
            y = y[:MAX_LEN]

        # Normalize
        mx = np.abs(y).max()
        if mx > 0:
            y = y / mx

        # Extract MFCC
        mfcc   = librosa.feature.mfcc(y=y, sr=SR, n_mfcc=N_MFCC,
                                        n_fft=512, hop_length=160)
        tensor = torch.tensor(mfcc, dtype=torch.float32).unsqueeze(0).unsqueeze(0)

        # Run model
        with torch.no_grad():
            out   = model(tensor)
            probs = torch.softmax(out, dim=1)[0].numpy()

        label      = 'REAL' if probs[0] > probs[1] else 'FAKE'
        confidence = float(max(probs[0], probs[1])) * 100

        # ── FIX 2: Language warning ───────────────────────────
        warning = None
        if lang and lang not in SUPPORTED_LANGUAGES:
            warning = (
                f'Note: The model was trained on English, Hindi, Kannada, '
                f'Marathi and Telugu only. Detection accuracy for other '
                f'languages may not be reliable.'
            )

        result = {
            'label':      label,
            'confidence': round(confidence, 1),
            'real_prob':  round(float(probs[0]) * 100, 1),
            'fake_prob':  round(float(probs[1]) * 100, 1),
        }
        if warning:
            result['warning'] = warning

        return result

    except Exception as e:
        return {'error': str(e), 'error_type': 'processing'}

# ── ROUTES ────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict_upload', methods=['POST'])
def predict_upload():
    if 'audio' not in request.files:
        return jsonify({'error': 'No file uploaded', 'error_type': 'input'})
    f      = request.files['audio']
    lang   = request.form.get('lang', None)   # optional lang from form
    suffix = Path(f.filename).suffix.lower() if f.filename else '.wav'
    if suffix not in ['.wav', '.mp3', '.webm', '.ogg', '.m4a', '.flac']:
        suffix = '.wav'
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        f.save(tmp.name)
        tmp_path = tmp.name
    result = predict(tmp_path, lang=lang)
    try:
        os.unlink(tmp_path)
    except:
        pass
    return jsonify(result)

@app.route('/predict_mic', methods=['POST'])
def predict_mic():
    data = request.get_json()
    if not data or 'audio' not in data:
        return jsonify({'error': 'No audio data received', 'error_type': 'input'})
    lang = data.get('lang', None)
    try:
        audio_bytes = base64.b64decode(data['audio'].split(',')[-1])
        with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
        result = predict(tmp_path, lang=lang)
        try:
            os.unlink(tmp_path)
        except:
            pass
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e), 'error_type': 'processing'})

@app.route('/samples/<path:filename>')
def serve_sample(filename):
    return send_from_directory(SAMPLES_DIR, filename)

if __name__ == '__main__':
    os.makedirs('templates',      exist_ok=True)
    os.makedirs('static/samples', exist_ok=True)
    print('\n🌐 VoiceGuard Web App starting...')
    print('   Open: http://localhost:5000\n')
    app.run(debug=True, port=5000)
