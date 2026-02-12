def generate_response(emotion):
    responses = {
        "joy": "That's awesome! Tell me more about it! 😄",
        "sadness": "I'm here for you. It's okay to feel this way. ❤️",
        "anger": "I understand your frustration. Want to talk about it? 😌",
        "fear": "It's okay to feel scared. You're not alone. 🤗",
        "disgust": "That sounds unpleasant. I get how you feel. 😕",
        "surprise": "Wow, that's unexpected! How do you feel about it?"
    }
    return responses.get(emotion.lower(), "I see. Tell me more!")
