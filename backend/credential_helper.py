import json
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


def load_env() -> None:
    """Load variables from a local .env.local file if present."""
    load_dotenv('.env.local')


def _cred_path() -> Path:
    return Path.home() / '.boaster' / 'credentials.json'


def get_api_key(name: str) -> Optional[str]:
    """Retrieve an API key from env vars or the local credential store."""
    load_env()
    if value := os.getenv(name):
        return value
    path = _cred_path()
    if path.exists():
        data = json.loads(path.read_text())
        providers = data.get('providers', {})
        return providers.get(name)
    return None
