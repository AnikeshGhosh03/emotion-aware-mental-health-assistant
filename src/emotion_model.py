# emotion_model.py
from transformers import pipeline

# Load pre-trained model
emotion_pipeline = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

def detect_emotion(text):
    result = emotion_pipeline(text)[0]
    # Pick the emotion with highest score
    top_emotion = max(result, key=lambda x: x['score'])
    return top_emotion['label'], top_emotion['score']
