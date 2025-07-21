import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime
from emotion_model import detect_emotion, auto_reply
from utils.trend_analysis import detect_negative_trend, send_email_alert
from utils.ollama_response import generate_ollama_reply  # NEW: Groq integration

st.set_page_config(page_title="Sentiment Watchdog", layout="wide")
LOG_FILE = "emotion_log.csv"

# Ensure log file exists
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=["timestamp", "role", "message", "emotion"]).to_csv(LOG_FILE, index=False)

def log_emotion(role, message, emotion):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = pd.DataFrame([[timestamp, role, message, emotion]], columns=["timestamp", "role", "message", "emotion"])
    entry.to_csv(LOG_FILE, mode="a", header=False, index=False)

def get_emotion_history():
    return pd.read_csv(LOG_FILE)

# ---------------- LOGIN SYSTEM ---------------- #

users = {
    "agent1": {"password": "sam1418", "role": "Agent"},
    "admin1": {"password": "adminpass", "role": "Admin"}
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

if not st.session_state.logged_in:
    st.title("🔐 Sentiment Watchdog Login")
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")

    username = username_input.strip().lower()
    password = password_input.strip()

    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = users[username]["role"]
            st.success(f"Welcome {username} ({st.session_state.role})!")
            st.rerun()
        else:
            st.error("Invalid credentials.")

# ---------------- MAIN APP ---------------- #

else:
    role = st.session_state.role
    st.sidebar.title("User Info")
    st.sidebar.write(f"👤 Logged in as: `{st.session_state.username}`")
    st.sidebar.write(f"🔑 Role: `{role}`")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()

    window = st.sidebar.slider("🕒 Trend Window Size", min_value=5, max_value=50, value=10)
    threshold = st.sidebar.slider("⚠️ Alert Threshold (%)", 10, 90, 50) / 100

    # ---------------------- AGENT SECTION ----------------------
    if role == "Agent":
        st.title("🎧 Agent Dashboard")
        st.subheader("✉️ Analyze a Single Message")

        user_input = st.text_area("Paste a support message:", height=150)

        if st.button("Analyze Emotion"):
            if user_input.strip():
                emotion, confidence = detect_emotion(user_input)
                st.success(f"**Emotion:** `{emotion}` ({confidence*100:.2f}%)")

                # 🔁 Groq-based reply
                reply = generate_ollama_reply(user_input, emotion)
                st.info(f"🤖 AI Response: {reply}")

                log_emotion("Agent", user_input, emotion)
                log_emotion("Agent", reply, "response")
            else:
                st.warning("Please enter a message.")

    # ---------------------- ADMIN SECTION ----------------------
    elif role == "Admin":
        st.title("📊 Admin Dashboard")

        st.subheader("📁 Upload Support Logs (CSV)")
        uploaded_file = st.file_uploader("Upload a CSV with a 'message' column")

        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            if 'message' not in df.columns:
                st.error("CSV must contain a column named 'message'.")
            else:
                with st.spinner("Analyzing messages..."):
                    df['emotion'], df['confidence'] = zip(*df['message'].astype(str).apply(detect_emotion))
                    for _, row in df.iterrows():
                        log_emotion("Batch", row['message'], row['emotion'])

                st.dataframe(df[['message', 'emotion', 'confidence']])
                st.bar_chart(df['emotion'].value_counts())

                st.subheader("📈 Sentiment Trend Alert")
                alert, message = detect_negative_trend(df['emotion'], window, threshold)

                if alert:
                    st.error(message)
                    if st.button("📧 Send Email Alert"):
                        success = send_email_alert(
                            "🚨 Negative Sentiment Spike Detected",
                            message,
                            "recipient_email@example.com"
                        )
                        st.success("Alert sent!" if success else "Failed to send alert.")
                else:
                    st.success(message)

                st.subheader("📤 Export Results")
                col1, col2 = st.columns(2)
                with col1:
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button("⬇️ Download CSV", csv, "emotion_results.csv", "text/csv")
                with col2:
                    df.to_excel("emotion_results.xlsx", index=False)
                    with open("emotion_results.xlsx", "rb") as f:
                        st.download_button("⬇️ Download Excel", f, "emotion_results.xlsx")

        st.subheader("📚 Emotion Log History")
        log_df = get_emotion_history()
        st.dataframe(log_df)

        st.download_button(
            "⬇️ Download Full Log CSV",
            log_df.to_csv(index=False).encode("utf-8"),
            "full_emotion_log.csv",
            "text/csv"
        )

        st.subheader("📡 Simulate Live Log Analysis")
        simulate = st.checkbox("Start Simulated Live Analysis")

        if simulate:
            if os.path.exists("data/sample_logs.csv"):
                df_stream = pd.read_csv("data/sample_logs.csv")
                emotions, messages = [], []
                alert_sent = False
                placeholder = st.empty()

                for idx, row in df_stream.iterrows():
                    msg = str(row["message"])
                    emo, _ = detect_emotion(msg)
                    messages.append(msg)
                    emotions.append(emo)
                    log_emotion("Simulated", msg, emo)

                    temp_df = pd.DataFrame({'message': messages, 'emotion': emotions})
                    alert, msg_alert = detect_negative_trend(temp_df['emotion'], window, threshold)

                    with placeholder.container():
                        st.markdown(f"**Latest Message:** {msg}")
                        st.markdown(f"**Detected Emotion:** `{emo}`")
                        st.bar_chart(temp_df['emotion'].value_counts())

                        if alert:
                            st.error(msg_alert)
                            if not alert_sent:
                                sent = send_email_alert(
                                    "🚨 Real-time Alert: Negative Sentiment Spike",
                                    msg_alert,
                                    "sumitkalamkar60@gmail.com"
                                )
                                st.success("📧 Auto Email Alert Sent!" if sent else "❌ Failed to auto-send alert.")
                                alert_sent = True
                        else:
                            st.success(msg_alert)

                    time.sleep(2)
            else:
                st.warning("No sample_logs.csv file found in /data.")
