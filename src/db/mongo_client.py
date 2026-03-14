import os
from pymongo import MongoClient
from datetime import datetime

# Get MongoDB URI from environment variable
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["emotion_chatbot"]
chat_collection = db["chat_history"]


def save_chat(user_input, bot_response, emotion, session_id="default"):

    chat_collection.insert_one({
        "session_id": session_id,
        "user": user_input,
        "bot": bot_response,
        "emotion": emotion,
        "timestamp": datetime.utcnow()
    })


def get_recent_chats(session_id="default", limit=5):

    chats = chat_collection.find(
        {"session_id": session_id},
        {"_id": 0}
    ).sort("timestamp", -1).limit(limit)

    return list(chats)[::-1]
