import os

class Settings:
    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    # Encryption for OpenAI API key (Fernet)
    FERNET_KEY = os.environ.get("FERNET_KEY")  # required
    ENCRYPTED_KEY_PATH = os.environ.get("ENCRYPTED_KEY_PATH", os.path.join(os.path.dirname(__file__), "api_key.enc"))

    # Google Sign-In
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")  # required if using Google login

    # DB
    DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "app.db"))

settings = Settings()
