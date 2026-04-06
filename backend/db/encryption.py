"""
Field-Level Encryption for HIPAA Compliance

Uses Fernet symmetric encryption for PII fields.
Key is loaded from ENCRYPTION_KEY environment variable.
Auto-generates key on first run if not set.
"""

import os
import hashlib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Load .env BEFORE checking for keys — this module may be imported
# before main.py's load_dotenv() runs
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
except ImportError:
    pass

_fernet = None


def _get_or_create_key():
    """Get encryption key from env or generate one."""
    key = os.getenv("ENCRYPTION_KEY")
    if key:
        return key.encode() if isinstance(key, str) else key

    # Auto-generate and save to .env for development
    from cryptography.fernet import Fernet
    new_key = Fernet.generate_key()

    env_path = Path(__file__).parent.parent / ".env"
    logger.warning("No ENCRYPTION_KEY found. Generating one and saving to %s", env_path)

    # Append to .env file
    with open(env_path, "a") as f:
        f.write(f"\nENCRYPTION_KEY={new_key.decode()}\n")

    os.environ["ENCRYPTION_KEY"] = new_key.decode()
    return new_key


def get_fernet():
    """Get or initialize the Fernet encryption instance."""
    global _fernet
    if _fernet is None:
        from cryptography.fernet import Fernet
        key = _get_or_create_key()
        _fernet = Fernet(key)
    return _fernet


def encrypt(plaintext):
    """Encrypt a string. Returns base64-encoded ciphertext."""
    if plaintext is None:
        return None
    if not isinstance(plaintext, str):
        plaintext = str(plaintext)
    return get_fernet().encrypt(plaintext.encode()).decode()


def decrypt(ciphertext):
    """Decrypt a base64-encoded ciphertext. Returns plaintext string."""
    if ciphertext is None:
        return None
    try:
        return get_fernet().decrypt(ciphertext.encode()).decode()
    except Exception as e:
        logger.error("Decryption failed: %s", e)
        return "[DECRYPTION_ERROR]"


def hash_for_lookup(value):
    """Create a deterministic SHA-256 hash for indexed lookups (e.g., email lookup).
    NOT reversible — used only for searching encrypted fields."""
    if value is None:
        return None
    normalized = value.strip().lower()
    return hashlib.sha256(normalized.encode()).hexdigest()


def encrypt_json(data):
    """Encrypt a dict/list as JSON string."""
    import json
    if data is None:
        return None
    return encrypt(json.dumps(data))


def decrypt_json(ciphertext):
    """Decrypt and parse JSON."""
    import json
    if ciphertext is None:
        return None
    try:
        plaintext = decrypt(ciphertext)
        if plaintext == "[DECRYPTION_ERROR]":
            return None
        return json.loads(plaintext)
    except (json.JSONDecodeError, Exception) as e:
        logger.error("JSON decryption failed: %s", e)
        return None
