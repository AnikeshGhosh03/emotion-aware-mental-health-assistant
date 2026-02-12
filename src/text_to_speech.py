import os
from gtts import gTTS
from datetime import datetime


def text_to_speech(text: str, lang: str = "en") -> str:
    """
    Convert text to speech and save as an MP3 file.
    Returns the file path of the generated audio.
    """
    try:
        if not text or text.strip() == "":
            return None

        # Create directory if it doesn't exist
        os.makedirs("temp_audio", exist_ok=True)

        # Unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_path = os.path.join("temp_audio", f"reply_{timestamp}.mp3")

        # Convert text to speech
        tts = gTTS(text=text, lang=lang)
        tts.save(audio_path)

        return audio_path

    except Exception as e:
        print(f"[TTS Error] {e}")
        return None
