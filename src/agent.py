def agent_action(emotion):
    """Decide the chatbot's action based on emotion."""
    actions = {
        "joy": "celebrate",
        "sadness": "comfort",
        "anger": "calm",
        "fear": "reassure",
        "disgust": "distract",
        "surprise": "acknowledge"
    }
    return actions.get(emotion.lower(), "neutral")
