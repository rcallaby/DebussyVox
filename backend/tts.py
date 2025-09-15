from gtts import gTTS
from pydub import AudioSegment
import os

def synthesize_text(text, out_path):
    """
    Uses gTTS to create an MP3 file at out_path.
    """
    # gTTS output is MP3
    tts = gTTS(text, lang="en")
    tmp = out_path + ".tmp.mp3"
    tts.save(tmp)

    # Optionally normalize with pydub and export as mp3
    sound = AudioSegment.from_file(tmp, format="mp3")
    sound.export(out_path, format="mp3")
    os.remove(tmp)
    return out_path
