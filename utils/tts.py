# utils/tts.py

from pathlib import Path
from gtts import gTTS
import hashlib

AUDIO_DIR = Path("audio")
AUDIO_DIR.mkdir(exist_ok=True)


def texto_para_audio(texto: str, lang: str = "pt") -> Path:
    h = hashlib.md5(texto.encode()).hexdigest()[:10]
    path = AUDIO_DIR / f"{h}.mp3"
    if not path.exists():
        tts = gTTS(text=texto, lang=lang)
        tts.save(path)
    return path
