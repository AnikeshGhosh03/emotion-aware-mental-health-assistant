# chatbot.py
from src.preprocessing import clean_text
from src.emotion_model import detect_emotion
from src.llm_response import get_ollama_response
from src.text_to_speech import text_to_speech
import csv, os

# ------------------- Negation Logic -------------------
negative_adjectives = [
    "unhappy", "sad", "angry", "upset", "disappointed", "tired", "afraid",
    "uncomfortable", "depressed", "nervous", "worried", "stressed", "annoyed",
    "lonely", "frustrated", "jealous", "miserable", "guilty", "hopeless",
    "scared", "terrified", "embarrassed", "ashamed", "hurt"
]

def handle_negation(sentence):
    """If negation precedes a negative adjective → return 'neutral'."""
    words = sentence.lower().split()
    for i, word in enumerate(words):
        if word == "not" and i + 1 < len(words):
            next_word = words[i + 1]
            if next_word in negative_adjectives:
                return "neutral"
    return None  # no correction needed
# ------------------------------------------------------

conversation_memory = []
LOG_FILE = "logs/chat_history.csv"
os.makedirs("logs", exist_ok=True)

# Create CSV log file if it doesn’t exist
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(["user_input", "bot_response", "emotion"])

def save_to_history(user_input, bot_response, emotion):
    """Save chat turn to history CSV."""
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([user_input, bot_response, emotion])

def chatbot_response(user_input):
    """Main chatbot function that connects all components."""
    # Step 1: Clean user input
    clean_input = clean_text(user_input)

    # Step 2: Detect emotion using the model
    emotion, _ = detect_emotion(clean_input)

    # Step 3: Apply negation rule to override emotion if needed
    neutral_check = handle_negation(user_input)
    if neutral_check == "neutral":
        emotion = "neutral"

    # Step 4: Prepare conversation history for LLM
    history_for_ollama = [{"user": u, "bot": b} for u, b, _ in conversation_memory]

    # Step 5: Generate AI reply
    reply_text, _ = get_ollama_response(user_input, emotion, history_for_ollama)

    # Step 6: Convert reply to speech
    audio_path = text_to_speech(reply_text)

    # Step 7: Log conversation
    conversation_memory.append((user_input, reply_text, emotion))
    save_to_history(user_input, reply_text, emotion)

    # Step 8: Return final outputs
    return {
        "bot": reply_text,
        "emotion": emotion,
        "audio": audio_path
    }
