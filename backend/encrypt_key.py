from cryptography.fernet import Fernet
import os

# Generate a Fernet key ONCE and store it in your shell env:
# python encrypt_key.py
# export FERNET_KEY='PASTE-PRINTED-KEY-HERE'
# This script will also create backend/api_key.enc

def main():
    fkey = Fernet.generate_key()
    print("Save this Fernet key (export as FERNET_KEY):", fkey.decode())
    cipher = Fernet(fkey)

    api_key = input("Enter your OpenAI API key (sk-...): ").strip().encode()
    enc = cipher.encrypt(api_key)

    out_path = os.path.join(os.path.dirname(__file__), "api_key.enc")
    with open(out_path, "wb") as f:
        f.write(enc)
    print(f"Encrypted key saved to {out_path}")

if __name__ == "__main__":
    main()
