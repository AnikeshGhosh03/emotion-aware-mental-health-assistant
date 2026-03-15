# chatbot.py

from src.preprocessing import clean_text
from src.emotion_model import detect_emotion
from src.llm_response import get_llm_response
from src.text_to_speech import text_to_speech
from src.db.mongo_client import save_chat, get_recent_chats


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

    return None


# ------------------------------------------------------


def chatbot_response(user_input, session_id="default"):
    """
    Main chatbot function that connects all components
    and uses MongoDB for conversation memory.
    """

    # Step 1: Clean user input
    clean_input = clean_text(user_input)

    # Step 2: Detect emotion
    emotion, _ = detect_emotion(clean_input)

    # Step 3: Apply negation correction
    neutral_check = handle_negation(user_input)

    if neutral_check == "neutral":
        emotion = "neutral"

    # Step 4: Fetch previous chats from MongoDB
    previous_chats = get_recent_chats(session_id, limit=5)

    history = [
        {"user": chat["user"], "bot": chat["bot"]}
        for chat in previous_chats
    ]

    # Step 5: Generate AI response (Hybrid LLM)
    reply_text, audio_path = get_llm_response(
        user_input,
        emotion,
        history
    )

    # Step 6: If audio not generated (fallback)
    if audio_path is None:
        audio_path = text_to_speech(reply_text)

    # Step 7: Save chat into MongoDB
    save_chat(user_input, reply_text, emotion, session_id)

    # Step 8: Return response
    return {
        "bot": reply_text,
        "emotion": emotion,
        "audio": audio_path
    }
