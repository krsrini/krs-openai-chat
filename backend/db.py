import sqlite3
from contextlib import contextmanager
from .config import settings
from werkzeug.security import generate_password_hash, check_password_hash

@contextmanager
def get_db():
    conn = sqlite3.connect(settings.DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()

def init_db():
    with get_db() as db:
        # Create users table if not exists
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT,
                provider TEXT DEFAULT 'local',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Add default admin user if not exists
        cur = db.execute("SELECT * FROM users WHERE username=?", ("admin",))
        if not cur.fetchone():
            hashed_pw = generate_password_hash("admin")  # store hashed password
            db.execute("INSERT INTO users (username, password_hash, provider) VALUES (?, ?, ?)",
                       ("admin", hashed_pw, "local"))
            print("Default admin user created: username=admin, password=admin")


def create_user(username, password=None, provider="local"):
    with get_db() as db:
        pwd_hash = generate_password_hash(password) if password else None
        db.execute("INSERT INTO users (username, password_hash, provider) VALUES (?, ?, ?)",
                   (username, pwd_hash, provider))

def get_user_by_username(username):
    with get_db() as db:
        cur = db.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cur.fetchone()

def verify_password(username, password):
    user = get_user_by_username(username)
    if not user or not user["password_hash"]:
        return False
    return check_password_hash(user["password_hash"], password)
