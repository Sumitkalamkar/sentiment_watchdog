from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

model_name = "j-hartmann/emotion-english-distilroberta-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
labels = model.config.id2label

def detect_emotion(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    outputs = model(**inputs)
    probs = F.softmax(outputs.logits, dim=1)
    top_prob, top_class = torch.max(probs, dim=1)
    return labels[top_class.item()], top_prob.item()

def auto_reply(emotion):
    replies = {
        "anger": "We’re really sorry for the inconvenience. Let us make this right.",
        "confusion": "We understand it’s unclear. Let me guide you step-by-step.",
        "joy": "Glad to hear that! We’re always here to help.",
        "sadness": "We’re sorry you feel this way. We’ll resolve it ASAP.",
        "neutral": "Thank you for reaching out. We’re looking into it.",
    }
    return replies.get(emotion, "Thanks for your message. We'll get back shortly.")
