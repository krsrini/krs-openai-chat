from flask import Flask, jsonify, request, session, send_from_directory
from flask_cors import CORS
import os
from .config import settings
from .db import init_db
from .openai_proxy import chat_completion
from .auth import auth_bp

app = Flask(__name__, static_folder="../frontend", static_url_path="/")
app.config["SECRET_KEY"] = settings.SECRET_KEY
CORS(app, supports_credentials=True)

# Blueprints
app.register_blueprint(auth_bp)

# Initialize DB at startup (Flask 3.x compatible)
with app.app_context():
    init_db()

# Serve frontend files
@app.route("/")
def root():
    return send_from_directory(app.static_folder, "login.html")

@app.route("/chat")
def chat_page():
    return send_from_directory(app.static_folder, "index.html")

# Session info
@app.route("/api/me", methods=["GET"])
def me():
    user = session.get("user")
    return jsonify({"username": user}) if user else jsonify({"username": None})

# Chat proxy
@app.route("/api/chat", methods=["POST"])
def chat_api():
    if not session.get("user"):
        return jsonify({"error": "unauthorized"}), 401

    payload = request.json or {}
    user_message = (payload.get("message") or "").strip()
    model = payload.get("model") or "gpt-4o-mini"
    if not user_message:
        return jsonify({"error": "message required"}), 400

    # You can pass history too if you want full context:
    # messages = payload.get("messages") or [{"role":"user","content":user_message}]
    messages = [{"role": "user", "content": user_message}]
    try:
        reply = chat_completion(messages, model)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run from repository root:  python -m backend.server
    app.run(host="127.0.0.1", port=5000, debug=True)
