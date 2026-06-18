from gtts import gTTS
import os

# ── Sentences per language ──────────────────────────────────────────────────
SENTENCES = {
    'en': [
        "Hello my name is Alex and I am speaking naturally.",
        "The weather today is very pleasant and sunny.",
        "Machine learning is a very interesting field of study.",
        "I enjoy listening to music in my free time.",
        "Voice cloning technology is advancing very rapidly.",
        "This is a test sentence for deepfake detection training.",
        "Artificial intelligence is changing the world around us.",
        "I went to the market to buy some vegetables today.",
        "Technology makes our daily life much more convenient.",
        "Reading books is a great habit for everyone.",
    ],
    'hi': [
        "नमस्ते मेरा नाम राहुल है और मैं दिल्ली में रहता हूं।",
        "आज मौसम बहुत अच्छा है और धूप भी निकली है।",
        "मशीन लर्निंग एक बहुत रोचक विषय है।",
        "मुझे संगीत सुनना बहुत पसंद है।",
        "कृत्रिम बुद्धिमत्ता हमारी दुनिया बदल रही है।",
        "मैं आज बाजार सब्जी लेने गया था।",
        "पढ़ाई करना जीवन में बहुत जरूरी है।",
        "भारत एक बहुत विविधताओं वाला देश है।",
        "मेरे परिवार में चार सदस्य हैं।",
        "खाना बनाना मुझे बहुत अच्छा लगता है।",
    ],
    'kn': [
        "ನಮಸ್ಕಾರ ನನ್ನ ಹೆಸರು ರಾಜ್ ಮತ್ತು ನಾನು ಬೆಂಗಳೂರಿನಲ್ಲಿ ವಾಸಿಸುತ್ತೇನೆ.",
        "ಇಂದು ಹವಾಮಾನ ತುಂಬಾ ಚೆನ್ನಾಗಿದೆ.",
        "ಯಂತ್ರ ಕಲಿಕೆ ತುಂಬಾ ಆಸಕ್ತಿದಾಯಕ ವಿಷಯ.",
        "ನನಗೆ ಸಂಗೀತ ಕೇಳುವುದು ತುಂಬಾ ಇಷ್ಟ.",
        "ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ ನಮ್ಮ ಜೀವನ ಬದಲಾಯಿಸುತ್ತಿದೆ.",
        "ನಾನು ಇಂದು ತರಕಾರಿ ತರಲು ಮಾರುಕಟ್ಟೆಗೆ ಹೋಗಿದ್ದೆ.",
        "ಕರ್ನಾಟಕ ತುಂಬಾ ಸುಂದರ ರಾಜ್ಯ.",
        "ನಮ್ಮ ಮನೆಯಲ್ಲಿ ನಾಲ್ಕು ಜನ ಇದ್ದಾರೆ.",
        "ಓದುವುದು ಒಳ್ಳೆಯ ಅಭ್ಯಾಸ.",
        "ತಂತ್ರಜ್ಞಾನ ನಮ್ಮ ದೈನಂದಿನ ಜೀವನ ಸುಲಭಗೊಳಿಸಿದೆ.",
    ],
    'te': [
        "నమస్కారం నా పేరు అర్జున్ మరియు నేను హైదరాబాద్‌లో నివసిస్తున్నాను.",
        "ఈరోజు వాతావరణం చాలా బాగుంది.",
        "మెషిన్ లెర్నింగ్ చాలా ఆసక్తికరమైన విషయం.",
        "నాకు సంగీతం వినడం చాలా ఇష్టం.",
        "కృత్రిమ మేధస్సు మన జీవితాన్ని మారుస్తోంది.",
        "నేను ఈరోజు కూరగాయలు కొనడానికి మార్కెట్‌కు వెళ్ళాను.",
        "తెలంగాణ చాలా అందమైన రాష్ట్రం.",
        "మా ఇంట్లో నలుగురు సభ్యులు ఉన్నారు.",
        "చదువు జీవితంలో చాలా ముఖ్యం.",
        "సాంకేతికత మన జీవితాన్ని సులభతరం చేసింది.",
    ],
    'mr': [
        "नमस्कार माझे नाव अमित आहे आणि मी पुण्यात राहतो.",
        "आज हवामान खूप छान आहे.",
        "मशीन लर्निंग हा खूप रोचक विषय आहे.",
        "मला संगीत ऐकणे खूप आवडते.",
        "कृत्रिम बुद्धिमत्ता आपले जीवन बदलत आहे.",
        "मी आज भाजी आणायला बाजारात गेलो होतो.",
        "महाराष्ट्र एक सुंदर राज्य आहे.",
        "आमच्या घरात चार माणसे आहेत.",
        "वाचन हे एक चांगले व्यसन आहे.",
        "तंत्रज्ञानाने आपले दैनंदिन जीवन सोपे केले आहे.",
    ],
}

# gTTS language codes
LANG_CODES = {
    'en': 'en',
    'hi': 'hi',
    'kn': 'kn',
    'te': 'te',
    'mr': 'mr',
}

# Output directory
OUTPUT_BASE = 'data/fake/gtts'

def generate_fake_audio():
    total = 0
    for lang, sentences in SENTENCES.items():
        lang_dir = os.path.join(OUTPUT_BASE, lang)
        os.makedirs(lang_dir, exist_ok=True)

        for i, sentence in enumerate(sentences):
            out_path = os.path.join(lang_dir, f'fake_{lang}_{i:03d}.wav')
            if os.path.exists(out_path):
                print(f'  [skip] {out_path} already exists')
                continue
            try:
                tts = gTTS(text=sentence, lang=LANG_CODES[lang])
                tts.save(out_path)
                total += 1
                print(f'  ✅ {out_path}')
            except Exception as e:
                print(f'  ❌ Error on {lang} sentence {i}: {e}')

    print(f'\n🎉 Done! Generated {total} fake audio files.')
    print(f'📁 Saved in: {OUTPUT_BASE}/')

generate_fake_audio()