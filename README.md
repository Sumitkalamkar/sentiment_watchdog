# 🐶 Sentiment Watchdog – AI-Powered Customer Support Assistant

**Sentiment Watchdog** is a real-time sentiment monitoring and auto-reply system built with **Streamlit**, designed for customer support teams to detect emotional trends, send empathetic replies, and prevent customer escalation.

---

## 🚀 Features

- ✅ Role-based login system (Agent/Admin)
- ✅ Real-time emotion detection (Hugging Face Transformers)
- ✅ Intelligent auto-reply generation (Groq API – LLaMA 3)
- ✅ CSV upload for bulk analysis
- ✅ Sentiment visualization (bar charts, logs)
- ✅ Simulated live log analysis
- ✅ Admin email alerts for spikes in negative sentiment
- ✅ Export logs as CSV and Excel

---

## 🧠 Tech Stack

- **Frontend:** Streamlit  
- **ML Model:** [joeddav/xlm-roberta-large-xnli](https://huggingface.co/joeddav/xlm-roberta-large-xnli)  
- **LLM Replies:** Groq API (LLaMA 3)  
- **Data Processing:** Pandas, Matplotlib  
- **Email Alerts:** SMTP via Gmail  
- **Auth & Logs:** Local CSV logic with static login

---

## 🔐 Login Credentials

> Default credentials to log in as either **Admin** or **Agent**:

| Role   | Username     | Password   |
|--------|--------------|------------|
| Admin  | `Admin1`      | `admin123`|
| Agent  | `Agent1`      | `sam1418` |

> You can customize these in `utils/auth.py`.

---

## 📁 Project Structure

```
customer_sentiment_watchdog/
├── app.py                         # Main Streamlit app
├── utils/
│   ├── auth.py                    # Role-based login
│   ├── detect_emotion.py         # Emotion classification
│   ├── ollama_response.py        # Reply generation (Groq API)
│   ├── trend_analysis.py         # Negative trend detection
├── data/
│   └── sample_chat.csv           # Sample customer messages
├── log_analysis.csv              # Generated sentiment logs
├── requirements.txt              # Python dependencies
├── .streamlit/
│   └── config.toml               # Streamlit UI theming
```

---

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YourUsername/sentiment_watchdog.git
   cd sentiment_watchdog
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

---

## 🔑 Configuration

### 1. Groq API Key

Open `utils/ollama_response.py`  
Replace:
```python
GROQ_API_KEY = "your_groq_api_key_here"
```
> ⚠️ Do **not** push the actual key to GitHub publicly.

### 2. Email Alerts (Optional)

If you want Admin email alerts for high negativity:

- Enable 2FA on your Gmail
- Create an App Password
- In `trend_analysis.py`, update:
```python
EMAIL_USER = "youremail@gmail.com"
EMAIL_PASS = "your_app_password"
```

---

## 🧪 Sample Data

Use `data/sample_chat.csv` to test batch analysis  
Or test live input from the app UI.

---

## ✨ Future Plans

- MongoDB support
- Admin dashboard
- Google OAuth login
- Real-time chat window
- Mobile UI support

---

## 🙋‍♂️ Author

Built solo by [Sumit Kalamkar](https://github.com/Sumitkalamkar) for a Hackathon 🏆  
**Where AI meets Empathy – One reply at a time.**

---

## 📄 License

This project is open source under the [MIT License](LICENSE).
