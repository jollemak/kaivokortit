import os
from dotenv import load_dotenv

load_dotenv()

def _require(name):
    value = os.getenv("MISTRAL_KEY")
    if not name:
        raise RuntimeError(f"{name} not found")
    return value

MISTRAL_KEY = _require("MISTRAL_KEY")

AZURE_STORAGE_CONNECTION_STRING=_require("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_KEY=_require("AZURE_STORAGE_KEY")

