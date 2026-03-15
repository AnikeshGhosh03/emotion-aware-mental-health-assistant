🎭 Emotion-Aware Mental Health Assistant

An intelligent Emotion-Aware AI Chatbot that detects a user’s emotional state from text or voice, generates empathetic responses using an LLM, and replies with both text and speech.

This system aims to act as a mental health support companion by understanding emotional context during conversations.

🚀 Features

🎤 Voice Input using microphone

🔊 Audio feedback before recording

🧠 Emotion Detection using Transformer models

🤖 Context-Aware AI Responses using an LLM

🗣️ Text-to-Speech Response

💬 Conversation Memory with MongoDB

🧾 Session-based Chat History

🌐 Interactive Web Interface with Streamlit

🧠 Emotions Detected

The chatbot uses the Hugging Face model
j-hartmann/emotion-english-distilroberta-base

Supported emotions:

Joy 😊

Neutral 😐

Sadness 😢

Anger 😠

Fear 😨

Surprise 😲

Disgust 🤢

⚠️ Note

The model does not detect:

Love ❤️

Sarcasm 😏

🏗️ Project Structure
emotion-aware-mental-health-assistant
│
├── app
│   ├── main.py              # Streamlit UI
│   └── static
│       └── avatar.png
│
├── src
│   ├── chatbot.py           # Main chatbot pipeline
│   ├── emotion_model.py     # Emotion detection
│   ├── preprocessing.py     # Text cleaning
│   ├── llm_response.py      # LLM response generator
│   ├── voice_to_text.py     # Speech recognition
│   ├── text_to_speech.py    # TTS generation
│   └── db
│       └── mongo_client.py  # MongoDB connection
│
├── requirements.txt
├── packages.txt
├── .gitignore
└── README.md
🧩 Tech Stack
Programming

Python 3.10+

Framework

Streamlit

Machine Learning

Hugging Face Transformers

DistilRoBERTa

Speech Processing

Faster Whisper

Text-to-Speech (TTS)

Database

MongoDB Atlas

LLM Backend

Ollama

⚙️ Installation
1️⃣ Clone the Repository
git clone https://github.com/AnikeshGhosh03/emotion-aware-mental-health-assistant.git
cd emotion-aware-mental-health-assistant
2️⃣ Create Virtual Environment
python -m venv venv

Activate environment:

Windows
venv\Scripts\activate
Linux / Mac
source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
▶️ Run the Application
streamlit run app/main.py

The chatbot will start on:

http://localhost:8501
🔊 Voice Interaction Flow

1. Click 🎤 Speak

2. Voice recording starts

3. Speech converted to text

4. Emotion detected

5. AI generates empathetic response

6. Response spoken via TTS

💾 Conversation Memory

All conversations are stored in:

MongoDB

Example document:

{
  "session_id": "user_1",
  "user": "I feel stressed",
  "bot": "I'm sorry you're feeling stressed. Want to talk about it?",
  "emotion": "sadness",
  "timestamp": "2026-03-15"
}

This allows the chatbot to maintain context across messages.

🔐 Security

Sensitive credentials are not stored in code.

Instead environment variables are used:

MONGO_URI = your_mongodb_connection_string
🛑 Limitations

Sarcasm detection not supported

Love emotion not detected

Primarily optimized for English

Microphone recording may not work on some cloud deployments

🔮 Future Improvements

Fine-tuned emotion classification model

Sarcasm detection module

Multilingual emotion recognition

Emotion-adaptive voice tone

Animated conversational UI

Mobile application version

👨‍💻 Author

Anikesh Ghosh

AI & Software Development Projects focused on:

Machine Learning

Conversational AI

Emotion Detection Systems

Data-Driven Applications

⭐ If You Like This Project

Give it a star ⭐ on GitHub!