# 🎭 Emotion-Aware Voice Chatbot Assistant

An intelligent **Emotion-Aware Voice Chatbot** that detects user emotions from text or voice, generates context-aware responses using an LLM, and replies with both **text and speech**.

---

## 🚀 Features

- 🎤 Voice input using microphone
- 🔊 Audio feedback (beep sound before recording)
- 🧠 Emotion detection using **DistilRoBERTa**
- 🤖 AI-generated responses using **Ollama / LLM**
- 🗣️ Text-to-Speech response
- 🧾 Chat history logging (CSV)
- 🌐 Streamlit-based UI

---

## 🧠 Emotions Detected

Using the pre-trained model  
`j-hartmann/emotion-english-distilroberta-base`

Supported emotions include:
- joy
- neutral
- sadness
- anger
- fear
- surprise
- disgust

> ⚠️ Note: Emotions like **love** and **sarcasm** are not detected by this model.

---

## 🏗️ Project Structure

emotion_chatbot/
│
├── app/
│ ├── main.py # Streamlit app
│ ├── chatbot.py # Main chatbot logic
│ └── static/
│ └── beep_sound.wav # Downloaded sound file
│
├── src/
│ ├── emotion_model.py # Emotion detection
│ ├── voice_to_text.py # Speech-to-text
│ ├── text_to_speech.py # Text-to-speech
│ ├── llm_response.py # LLM response handler
│ └── preprocessing.py # Text cleaning
│
├── logs/
│ └── chat_history.csv
│
├── requirements.txt
└── README.md


---

## 🧩 Tech Stack

- Python 3.10+
- Streamlit
- Hugging Face Transformers
- Faster-Whisper
- SoundDevice / SimpleAudio
- Ollama (LLM backend)

---

## ⚙️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/AnikeshGhosh03/emotion-aware-mental-health-assistant.git
cd emotion_chatbot

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

▶️ Run the Application
streamlit run app/main.py

🔊 Audio Recording Behavior

Click 🎤 Speak button

Button turns red

Beep sound plays

Records for 7 seconds

Button resets automatically

🧪 Model Used
Emotion Model:
j-hartmann/emotion-english-distilroberta-base

📁 Logs

All conversations are stored in:

logs/chat_history.csv

🛑 Limitations

Sarcasm detection not supported

Love emotion not classified

English language only

🔮 Future Improvements

Fine-tuned emotion model

Sarcasm detection

Multilingual support

Emotion-specific voice modulation

UI animations
