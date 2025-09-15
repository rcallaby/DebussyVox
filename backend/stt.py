import speech_recognition as sr
from pydub import AudioSegment
import os

def transcribe_file(filepath):
    """
    Convert common audio formats to WAV (if needed) and transcribe using recognizer (Google Web Speech).
    """
    r = sr.Recognizer()

    # Convert to WAV 16k mono using pydub for better compatibility
    base, ext = os.path.splitext(filepath)
    wav_path = base + ".wav"
    # If already .wav, just use it
    if ext.lower() != ".wav":
        sound = AudioSegment.from_file(filepath)
        sound = sound.set_frame_rate(16000).set_channels(1)
        sound.export(wav_path, format="wav")
    else:
        wav_path = filepath

    with sr.AudioFile(wav_path) as source:
        audio_data = r.record(source)

    # Use Google's free web API (requires network)
    text = r.recognize_google(audio_data)
    # cleanup temp wav if we created it
    if wav_path != filepath and os.path.exists(wav_path):
        os.remove(wav_path)
    return text
