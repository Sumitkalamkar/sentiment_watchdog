import smtplib
from email.message import EmailMessage
import pandas as pd
from collections import Counter
from dotenv import load_dotenv
import os
import csv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()
EMAIL = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


def detect_negative_trend(emotion_series: pd.Series, window: int = 5, threshold: int = 3):
    """
    Detects a negative sentiment trend in the last `window` entries.
    Returns (is_negative_trend: bool, message: str)
    """
    negative_emotions = ["anger", "fear", "sadness"]
    last_emotions = emotion_series.tail(window)

    negative_count = sum(1 for e in last_emotions if e in negative_emotions)

    if negative_count >= threshold:
        emotion_counts = Counter(last_emotions)
        top_neg = emotion_counts.most_common(1)[0][0]
        return True, (
            f"⚠️ Negative sentiment detected!\n\n"
            f"Recent emotions: {', '.join(last_emotions)}\n"
            f"Dominant emotion: {top_neg.upper()}"
        )
    else:
        return False, "✅ No negative trend detected in recent customer emotions."


def send_email_alert(subject: str, content: str, to_email: str):
    """
    Sends an email alert with the given subject and content.
    Returns True if successful, False otherwise.
    """
    try:
        msg = EmailMessage()
        msg.set_content(content)
        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = to_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL, EMAIL_PASS)
            smtp.send_message(msg)

        print("✅ Email alert sent successfully!")
        return True
    except Exception as e:
        print("❌ Failed to send email:", e)
        return False


def append_log(emotion: str, alert_triggered: bool, message: str, file_path: str = "log_analysis.csv"):
    """
    Appends a new entry to the log_analysis.csv file.
    Auto-creates the file with headers if not present.
    """
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "emotion": emotion,
        "alert_triggered": alert_triggered,
        "message": message
    }

    file_exists = os.path.isfile(file_path)

    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=log_entry.keys())

        if not file_exists:
            writer.writeheader()
        writer.writerow(log_entry)
