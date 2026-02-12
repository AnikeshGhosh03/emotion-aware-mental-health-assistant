import streamlit as st
import pandas as pd
import logs.chat_history

st.set_page_config(page_title="Mood Analytics Dashboard 📊", layout="wide")
st.title("Mood Analytics Dashboard 📊")

# Load chat history
history = load_chat_history()

if not history:
    st.warning("No chat history found yet.")
else:
    df = pd.DataFrame(history)
    st.write("### Recent Chats")
    st.dataframe(df.tail(10), use_container_width=True)

    # Count emotions
    emotion_counts = df['emotion'].value_counts()

    # Display bar chart
    st.write("### Emotion Frequency")
    st.bar_chart(emotion_counts)

    # Positive vs Negative Pie Chart
    positive = ["joy", "surprise"]
    df["sentiment"] = df["emotion"].apply(lambda x: "Positive" if x in positive else "Negative")
    st.write("### Sentiment Split")
    st.bar_chart(df["sentiment"].value_counts())
