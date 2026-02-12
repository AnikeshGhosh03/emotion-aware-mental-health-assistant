# main.py
import sys, os, base64
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from PIL import Image
from src.chatbot import chatbot_response
from src.voice_to_text import record_audio, save_wav, model  # For speech input

# --- Page Config ---
st.set_page_config(page_title="Emotion Detection Chatbot 🤖💬", layout="wide")

# --- Load Avatar ---
avatar_path = r"C:\Users\anike\PycharmProjects\pythonProject\emotion_chatbot\app\static\898f884c-7439-4ab0-97ce-3a818a533068.png"
avatar = Image.open(avatar_path) if os.path.exists(avatar_path) else None

# --- Header ---
col1, col2 = st.columns([1, 4])
with col1:
    if avatar:
        st.image(avatar, width=120)
with col2:
    st.markdown("<h1 style='color:#4A90E;'>Emotion Detection Chatbot 🤖💬</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:gray;'>Your empathetic AI companion</p>", unsafe_allow_html=True)

st.write("---")

# --- Session States ---
if "history" not in st.session_state:
    st.session_state.history = []
if "temp_input" not in st.session_state:
    st.session_state.temp_input = ""
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# --- Layout ---
left_col, right_col = st.columns([1, 2])

# --- Left Column: Chat History ---
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

# --- Right Column: Live Chat ---
with right_col:
    st.subheader("💬 Live Chat")

    # Display chat messages dynamically
    for chat in st.session_state.history:
        with st.chat_message("user"):
            st.write(chat["user"])
        with st.chat_message("assistant"):
            st.write(f"**({chat['emotion']})** {chat['bot']}")
            if chat.get("audio"):
                st.audio(chat["audio"], format="audio/mp3")

    # --- Text Input Field ---
    user_input = st.text_input(
        "Type your message or speak...",
        value=st.session_state.user_input or st.session_state.temp_input,
        key="chat_input"
    )

    # --- Buttons ---
    col_btn1, col_btn2 = st.columns([1, 1])

    # 🎤 Record voice and transcribe
    with col_btn1:
        speak_placeholder = st.empty()

        if st.button("🎤 Speak"):
            try:
                # Change button color to red while recording
                with speak_placeholder.container():
                    st.markdown(
                        """
                        <style>
                            div[data-testid="stButton"] button {
                                background-color: red !important;
                                color: white !important;
                            }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )
                   # st.info("🎙 Speak now... (you have 7 seconds)")

                # Record for exactly 7 seconds
                audio_data, sr = record_audio(duration=7)
                wav_path = save_wav(audio_data, sr)

                # Transcribe speech
                segments, _ = model.transcribe(wav_path)
                transcribed_text = " ".join([seg.text for seg in segments])
                st.session_state.temp_input = transcribed_text

                # Cleanup
                os.remove(wav_path)

                # Reset UI color
                st.markdown(
                    """
                    <style>
                        div[data-testid="stButton"] button {
                            background-color: #f0f2f6 !important;
                            color: black !important;
                        }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                st.success("✅ Speech transcribed successfully!")
                st.rerun()

            except Exception as e:
                st.error(f"❌ Voice input failed: {e}")

    # 💬 Send message
    with col_btn2:
        if st.button("Send") and user_input.strip():
            try:
                result = chatbot_response(user_input)

                # Save to history
                st.session_state.history.append({
                    "user": user_input,
                    "bot": result["bot"],
                    "emotion": result["emotion"],
                    "audio": result["audio"]
                })

                # Show messages instantly
                with st.chat_message("user"):
                    st.write(user_input)
                with st.chat_message("assistant"):
                    st.write(f"**({result['emotion']})** {result['bot']}")

                # 🔊 Auto-play TTS in background
                if result["audio"] and os.path.exists(result["audio"]):
                    with open(result["audio"], "rb") as f:
                        audio_base64 = base64.b64encode(f.read()).decode()
                    st.markdown(
                        f"""
                        <audio autoplay hidden>
                            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                        </audio>
                        """,
                        unsafe_allow_html=True
                    )

                # 🧹 Clear text input after sending
                st.session_state.user_input = ""
                st.session_state.temp_input = ""
                st.rerun()

            except Exception as e:
                st.error(f"❌ Error generating response: {e}")
