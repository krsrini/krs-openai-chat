import os
import json
import requests
from cryptography.fernet import Fernet
from .config import settings

def get_openai_api_key():
    if not settings.FERNET_KEY:
        raise RuntimeError("FERNET_KEY missing in environment")
    cipher = Fernet(settings.FERNET_KEY)
    with open(settings.ENCRYPTED_KEY_PATH, "rb") as f:
        enc = f.read()
    return cipher.decrypt(enc).decode()

def chat_completion(messages, model):
    api_key = get_openai_api_key()
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7
    }
    resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=120)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]
