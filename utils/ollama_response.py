import requests
import os

def generate_ollama_reply(text, emotion):
   GROQ_API_KEY = "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"

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",  # Change if using another model
        "messages": [
            {"role": "system", "content": f"You are an empathetic customer support assistant that responds based on the user's emotion: {emotion}"},
            {"role": "user", "content": text}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        # Debug output to log
        print("Groq API response:", data)

        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        elif "error" in data:
            return f"❌ API error: {data['error'].get('message', str(data['error']))}"
        else:
            return "❌ Unexpected API response format."

    except Exception as e:
        return f"❌ Exception while calling Groq API: {str(e)}"
