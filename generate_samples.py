"""
generate_samples.py
Run this ONCE to generate the sample audio files used on the website.
Place this file in your AICS PROJECT folder and run: python generate_samples.py
"""

from gtts import gTTS
from pathlib import Path

Path('static/samples').mkdir(parents=True, exist_ok=True)

FAKE_SAMPLES = {
    'fake_english.wav': ('Hello, this is an AI generated voice sample for deepfake detection testing.', 'en'),
    'fake_hindi.wav':   ('नमस्ते, यह एक कृत्रिम बुद्धिमत्ता द्वारा बनाई गई आवाज़ है।', 'hi'),
    'fake_kannada.wav': ('ನಮಸ್ಕಾರ, ಇದು ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆಯಿಂದ ರಚಿಸಲಾದ ಧ್ವನಿ.', 'kn'),
    'fake_marathi.wav': ('नमस्कार, ही कृत्रिम बुद्धिमत्तेने तयार केलेली आवाज आहे.', 'mr'),
    'fake_telugu.wav':  ('నమస్కారం, ఇది కృత్రిమ మేధస్సు ద్వారా రూపొందించిన గొంతు.', 'te'),
}

print('Generating fake sample audio files...')
for filename, (text, lang) in FAKE_SAMPLES.items():
    out_path = f'static/samples/{filename}'
    if Path(out_path).exists():
        print(f'  [skip] {filename} already exists')
        continue
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(out_path)
        print(f'  [OK]   {filename}')
    except Exception as e:
        print(f'  [ERR]  {filename}: {e}')

print('\nDone!')
print()
print('NOTE: For REAL sample files, copy these from your dataset:')
print('  data/real/english/*.wav  ->  static/samples/real_english.wav  (copy any one file)')
print('  data/real/hindi/*.mp3    ->  static/samples/real_hindi.wav    (rename to .wav)')
print('  data/real/kannada/*.mp3  ->  static/samples/real_kannada.wav')
print('  data/real/marathi/*.mp3  ->  static/samples/real_marathi.wav')
print('  data/real/telugu/*.mp3   ->  static/samples/real_telugu.wav')
print()
print('Then run: python app.py')
print('Open:     http://localhost:5000')
