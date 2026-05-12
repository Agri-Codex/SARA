import base64
import os
from pathlib import Path
from sara_assistant.config import DATA_DIR

VAULT_FILE = DATA_DIR / "secure_vault.dat"


class SecurityManager:
    """Lightweight local vault placeholder.

    This is not enterprise encryption. For production, replace with Windows Credential Manager
    or a proper encrypted keyring backend.
    """

    @staticmethod
    def mask_secret(value: str) -> str:
        if not value:
            return ""
        if len(value) <= 8:
            return "*" * len(value)
        return value[:4] + "*" * (len(value) - 8) + value[-4:]

    @staticmethod
    def save_token(name: str, token: str):
        DATA_DIR.mkdir(exist_ok=True)
        encoded = base64.b64encode(f"{name}:{token}".encode("utf-8")).decode("utf-8")
        VAULT_FILE.write_text(encoded, encoding="utf-8")
        return "Token saved in local vault placeholder."

    @staticmethod
    def read_token():
        if not VAULT_FILE.exists():
            return None
        try:
            decoded = base64.b64decode(VAULT_FILE.read_text(encoding="utf-8")).decode("utf-8")
            return decoded
        except Exception:
            return None

    @staticmethod
    def security_report() -> str:
        checks = [
            "Local command confirmation enabled for shutdown.",
            "API key should be stored in .env or secure vault.",
            "Dangerous automation must stay confirmation-gated.",
            "Production encryption still requires Windows Credential Manager/keyring.",
        ]
        return "Security report: " + " | ".join(checks)
