# KRS Local OpenAI Chat

Features:
- Username/password auth + Google Sign-In
- Secure backend proxy (OpenAI key encrypted with Fernet)
- Markdown rendering with syntax highlighting + "Copy" buttons
- Timestamps per message
- LocalStorage chat history per user
- “Thinking…” animated indicator

## Setup

1) Create and activate a virtualenv, then install deps:

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

