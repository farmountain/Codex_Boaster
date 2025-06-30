import os
import json
from pathlib import Path

SECRETS_FILE = Path(os.getenv("SECRETS_FILE", "secrets.json"))

def get_secret(name: str) -> str | None:
    """Return secret from env or optional secrets.json."""
    if value := os.getenv(name):
        return value
    if SECRETS_FILE.exists():
        try:
            data = json.loads(SECRETS_FILE.read_text())
            return data.get(name)
        except Exception:
            return None
    return None
