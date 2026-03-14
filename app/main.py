# main.py
import sys, os, base64
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from PIL import Image
from src.chatbot import chatbot_response
from src.voice_to_text import record_audio, save_wav, model

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Emotion Detection Chatbot 🤖💬", layout="wide")

# ---------------- AVATAR ----------------
avatar_path = r"C:\Users\anike\Desktop\emotion_chatbot\app\static\Assistant.png"
avatar = Image.open(avatar_path) if os.path.exists(avatar_path) else None

SESSION_ID = "streamlit_user"

# ---------------- SESSION STATES ----------------
if "history" not in st.session_state:
    st.session_state.history = []

if "chat_input" not in st.session_state:
    st.session_state.chat_input = ""

if "temp_input" not in st.session_state:
    st.session_state.temp_input = ""

# ---------------- SEND FUNCTION ----------------
def send_message():

    user_input = st.session_state.chat_input.strip()

    if user_input:

        result = chatbot_response(user_input, SESSION_ID)

        st.session_state.history.append({
            "user": user_input,
            "bot": result["bot"],
            "emotion": result["emotion"],
            "audio": result["audio"]
        })

    # Clear input box
    st.session_state.chat_input = ""


# ---------------- HEADER ----------------
col1, col2 = st.columns([1, 4])

with col1:
    if avatar:
        st.image(avatar, width=120)

with col2:
    st.markdown(
        "<h1 style='color:#4A90E;'>Emotion Detection Chatbot 🤖💬</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='color:gray;'>Your empathetic AI companion</p>",
        unsafe_allow_html=True
    )

st.write("---")

# ---------------- LAYOUT ----------------
left_col, right_col = st.columns([1, 2])

# ================= LEFT PANEL =================
with left_col:

    st.subheader("🗂 Previous Chats")

    if st.session_state.history:

        for i, chat in enumerate(st.session_state.history, 1):

            st.markdown(
                f"<b>{i}. You:</b> {chat['user']}<br>"
                f"<b style='color:#4A90E;'>Bot:</b> {chat['bot']} "
                f"<small>({chat['emotion']})</small>",
                unsafe_allow_html=True
            )

            st.markdown("<hr>", unsafe_allow_html=True)

    else:
        st.info("No previous messages yet. Start chatting!")

# ================= RIGHT PANEL =================
with right_col:

    st.subheader("💬 Live Chat")

    for chat in st.session_state.history:

        with st.chat_message("user"):
            st.write(chat["user"])

        with st.chat_message("assistant"):
            st.write(f"**({chat['emotion']})** {chat['bot']}")

            if chat.get("audio"):
                st.audio(chat["audio"], format="audio/mp3")

    # ----------- INPUT BOX -----------
    st.text_input(
        "Type your message or speak...",
        key="chat_input"
    )

    col_btn1, col_btn2 = st.columns([1, 1])

    # 🎤 VOICE INPUT
    with col_btn1:

        if st.button("🎤 Speak"):

            try:
                st.info("Recording for 7 seconds...")

                audio_data, sr = record_audio(duration=7)
                wav_path = save_wav(audio_data, sr)

                segments, _ = model.transcribe(wav_path)
                transcribed_text = " ".join([seg.text for seg in segments])

                st.session_state.chat_input = transcribed_text

                os.remove(wav_path)

                st.success("Speech transcribed successfully!")

            except Exception as e:
                st.error(f"Voice input failed: {e}")

    # 💬 SEND BUTTON
    with col_btn2:

        st.button("Send", on_click=send_message)
