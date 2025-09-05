from flask import Blueprint, request, session, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from .db import init_db, create_user, get_user_by_username, verify_password
from .config import settings

auth_bp = Blueprint("auth", __name__, url_prefix="/api")

@auth_bp.route("/signup", methods=["POST"])
def signup():
    payload = request.json or {}
    username = (payload.get("username") or "").strip().lower()
    password = payload.get("password") or ""
    if not username or not password:
        return jsonify({"error": "username and password required"}), 400
    if get_user_by_username(username):
        return jsonify({"error": "username already exists"}), 409
    create_user(username, password, provider="local")
    return jsonify({"ok": True})


@auth_bp.route("/login", methods=["POST"])
def login():
    payload = request.json or {}
    username = (payload.get("username") or "").strip().lower()
    password = payload.get("password") or ""

    # Default admin login
    if username == "admin" and password == "admin":
        session["user"] = "admin"
        return jsonify({"ok": True, "username": "admin"})

    # Local DB login
    if not verify_password(username, password):
        return jsonify({"error": "invalid credentials"}), 401

    session["user"] = username
    return jsonify({"ok": True, "username": username})


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"ok": True})


@auth_bp.route("/google-login", methods=["POST"])
def google_login():
    if not settings.GOOGLE_CLIENT_ID:
        return jsonify({"error": "GOOGLE_CLIENT_ID not configured"}), 500

    token = (request.json or {}).get("id_token")
    if not token:
        return jsonify({"error": "missing id_token"}), 400

    try:
        idinfo = id_token.verify_oauth2_token(token, grequests.Request(), settings.GOOGLE_CLIENT_ID)
        username = (idinfo.get("email") or "").lower()
        if not username:
            return jsonify({"error": "invalid token"}), 400

        # Ensure user exists
        if not get_user_by_username(username):
            create_user(username, password=None, provider="google")

        session["user"] = username
        return jsonify({"ok": True, "username": username})
    except Exception as e:
        return jsonify({"error": str(e)}), 401
