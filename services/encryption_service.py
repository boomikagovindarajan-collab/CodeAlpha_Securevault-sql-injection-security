import os
import base64
import hashlib
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()


def get_cipher():
    encryption_secret = os.getenv(
        "ENCRYPTION_KEY",
        "securevault_default_encryption_key"
    )

    key_bytes = hashlib.sha256(
        encryption_secret.encode()
    ).digest()

    fernet_key = base64.urlsafe_b64encode(key_bytes)

    return Fernet(fernet_key)


cipher = get_cipher()


def encrypt_data(plain_text):
    return cipher.encrypt(plain_text.encode()).decode()


def decrypt_data(encrypted_text):
    return cipher.decrypt(encrypted_text.encode()).decode()