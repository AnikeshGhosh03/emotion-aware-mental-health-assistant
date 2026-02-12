# voice_to_text.py
import sounddevice as sd
import numpy as np
import tempfile
import wave
import os
from faster_whisper import WhisperModel

# --- Load Whisper model once globally ---
try:
    print("🔄 Loading Whisper model...")
    model = WhisperModel("large-v3", device="cpu")  # Change to "cuda" for GPU
    print("✅ Whisper model loaded successfully.")
except Exception as e:
    model = None
    print(f"Failed to load Whisper model: {e}")

BEEP_PATH = r"C:\Users\anike\Desktop\emotion_chatbot\voice_to_text\mixkit-select-click-1109.wav"
def play_beep():
    """Play a short beep sound to signal recording start."""
    if os.path.exists(BEEP_PATH):
        try:
            wave_obj = sa.WaveObject.from_wave_file(BEEP_PATH)
            play_obj = wave_obj.play()
            play_obj.wait_done()
        except Exception as e:
            print(f"⚠️ Failed to play beep sound: {e}")
    else:
        print(f"⚠️ Beep file not found at: {BEEP_PATH}")


def record_audio(duration=7, samplerate=16000):
    """Record audio from the microphone."""
    try:
        # 🔊 Play beep to indicate start
        play_beep()

        print(f"🎙 Recording for {duration} seconds...")
        audio_data = sd.rec(
            int(duration * samplerate),
            samplerate=samplerate,
            channels=1,
            dtype=np.int16
        )
        sd.wait()
        print(" Recording finished.")
        return audio_data, samplerate
    except Exception as e:
        print(f" Error recording audio: {e}")
        return None, None



def save_wav(audio_data, samplerate):
    """Save recorded audio to a temporary WAV file."""
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        with wave.open(temp_file.name, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(samplerate)
            wf.writeframes(audio_data.tobytes())
        return temp_file.name
    except Exception as e:
        print(f"❌ Error saving WAV file: {e}")
        return None


def transcribe_audio(file_path):
    """Transcribe audio using Whisper."""
    if model is None:
        return ""

    try:
        segments, _ = model.transcribe(file_path)
        return " ".join([seg.text.strip() for seg in segments])
    except Exception as e:
        print(f"❌ Transcription failed: {e}")
        return ""
