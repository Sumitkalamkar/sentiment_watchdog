import requests
import os

GROQ_API_KEY = "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"  # This will be loaded from Streamlit Secrets

GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

def generate_ollama_reply(message, emotion, model='llama3-8b-8192'):
    prompt = f"""
You are a helpful customer support agent.

The customer message is:
\"{message}\"

The detected emotion is: {emotion}.

Based on this, write a short, polite, and empathetic reply.
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(GROQ_ENDPOINT, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]
