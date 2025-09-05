# KRS Local Chat with OpenAI

A local web-based chat interface to interact with OpenAI models.  
Supports login/signup, Google authentication, and secure key handling.  
Built with **Flask (backend)** + **HTML/CSS/JS (frontend)**.

---

## ✨ Features
- 🔑 **Authentication**
  - Local login/signup
  - Default `admin/admin` account
  - Google OAuth login
- 💬 **Chat with OpenAI**
  - Rich text & formatted code output
  - “Thinking…” animation while waiting
  - Chat history with timestamp
- 🔒 **Secure key storage**
  - API key encryption using `Fernet`
- 📦 Modular backend (ready for GitHub)

---

## 📂 Project Structure
krs-openai-chat/
├── backend/
│ ├── server.py # Flask app entrypoint
│ ├── auth.py # Authentication routes
│ ├── db.py # SQLite + user management
│ ├── config.py # App settings
│ ├── openai_proxy.py # OpenAI API calls
│ └── ...
├── frontend/
│ ├── index.html # Chat UI
│ ├── login.html # Login/Signup UI
│ └── style.css # Styling
├── requirements.txt
├── .gitignore
└── README.md


---

## 🚀 Getting Started

### 1. Clone repo & setup venv

git clone https://github.com/krsrini/krs-openai-chat.git
cd krs-openai-chat
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

### 2. Configure environment

Create .env in backend/:

SECRET_KEY="your-flask-secret-key"
FERNET_KEY="your-fernet-key"   # Run: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
GOOGLE_CLIENT_ID="your-google-client-id.apps.googleusercontent.com"

### 3. Store OpenAI API key

Encrypt your OpenAI API key:

python backend/crypto_util.py encrypt "sk-your-api-key"

### 4. Run server

python -m backend.server

Open http://127.0.0.1:5000 🎉

🗝️ Default Login

Username: admin
Password: admin

(You should change/remove this in production)

🛠️ Tech Stack

Backend: Flask, SQLite, Werkzeug, Google Auth
Frontend: HTML, CSS, JS
AI: OpenAI GPT models