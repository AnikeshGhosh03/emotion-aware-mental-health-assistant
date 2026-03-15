import requests
import json
import os
from datetime import datetime
from gtts import gTTS
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

load_dotenv()

# Get API key safely (local + streamlit cloud)
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        api_key = None

# Initialize OpenAI client only if key exists
openai_client = OpenAI(api_key=api_key) if api_key else None

# Detect cloud environment
IS_CLOUD = os.getenv("STREAMLIT_RUNTIME") is not None


def get_ollama_response(
    user_message: str,
    emotion: str,
    history=None,
    model: str = "gemma:2b"
) -> tuple:

    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}

    # --- Conversation history ---
    history_text = ""
    if history:
        for turn in history[-5:]:
            history_text += f"User: {turn.get('user','')}\nAI: {turn.get('bot','')}\n"

    prompt = f"""
    The user is feeling {emotion}.
    You are a warm, caring AI companion.
    Respond naturally with empathy, short sentences.

    Conversation so far:
    {history_text}

    New message:
    User: {user_message}
    AI:
    """

    payload = {"model": model, "prompt": prompt.strip(), "stream": False}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()

        output = ""
        for line in response.text.splitlines():
            try:
                part = json.loads(line)
                if "response" in part:
                    output += part["response"]
            except json.JSONDecodeError:
                continue

        reply_text = output.strip()

    except Exception as e:
        return f"[Ollama Error: {e}]", None

    return generate_tts(reply_text)


def get_openai_response(user_message: str, emotion: str, history=None) -> tuple:

    history_text = ""
    if history:
        for turn in history[-5:]:
            history_text += f"User: {turn.get('user','')}\nAI: {turn.get('bot','')}\n"

    prompt = f"""
    The user is feeling {emotion}.
    You are a compassionate mental health assistant.
    Respond with empathy and supportive tone.

    Conversation so far:
    {history_text}

    User: {user_message}
    AI:
    """

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an empathetic mental health assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        reply_text = response.choices[0].message.content.strip()

    except Exception as e:
        return f"[OpenAI Error: {e}]", None

    return generate_tts(reply_text)


def generate_tts(reply_text: str):
    """Generate audio using gTTS"""

    try:
        os.makedirs("temp_audio", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_path = os.path.join("temp_audio", f"reply_{timestamp}.mp3")

        tts = gTTS(text=reply_text, lang="en")
        tts.save(audio_path)

        return reply_text, audio_path

    except Exception as e:
        print(f"[TTS Error] {e}")
        return reply_text, None


def get_llm_response(user_message: str, emotion: str, history=None) -> tuple:
    """
    Automatically choose the correct LLM.
    """

    if IS_CLOUD:
        return get_openai_response(user_message, emotion, history)

    else:
        return get_ollama_response(user_message, emotion, history)