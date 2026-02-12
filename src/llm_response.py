import requests
import json
from gtts import gTTS
import os
from datetime import datetime


def get_ollama_response(
    user_message: str,
    emotion: str,
    history=None,
    model: str = "gemma:2b"
) -> tuple:
    """
    Generate empathetic, human-like replies using Ollama API and convert to speech.

    Returns:
        (text_reply, audio_path)
    """

    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}

    # --- Build conversation context ---
    history_text = ""
    if history:
        for turn in history[-5:]:
            history_text += f"User: {turn.get('user', '')}\nAI: {turn.get('bot', '')}\n"

    # --- Prompt for response generation ---
    prompt = f"""
    The user is feeling {emotion}.
    You are a warm, caring AI companion.
    Respond naturally with empathy, short sentences, and an emotionally intelligent tone.

    Conversation so far:
    {history_text}

    New message:
    User: {user_message}
    AI:
    """

    payload = {"model": model, "prompt": prompt.strip(), "stream": False}

    try:
        # --- Send request to Ollama ---
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()

        # --- Parse response text ---
        output = ""
        for line in response.text.splitlines():
            try:
                part = json.loads(line)
                if "response" in part:
                    output += part["response"]
            except json.JSONDecodeError:
                continue

        reply_text = output.strip() if output else "No response from Ollama."

        # --- Generate TTS using gTTS ---
        audio_path = None
        try:
            os.makedirs("temp_audio", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_path = os.path.join("temp_audio", f"reply_{timestamp}.mp3")

            tts = gTTS(text=reply_text, lang="en")
            tts.save(audio_path)

        except Exception as tts_error:
            print(f"[TTS Error] {tts_error}")
            audio_path = None

        return reply_text, audio_path

    except Exception as e:
        return f"[Error connecting to Ollama: {e}]", None
