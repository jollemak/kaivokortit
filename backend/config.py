import os
from dotenv import load_dotenv

def __require(name, value):
    if not value:
        raise RuntimeError(f"{name} not found")
    return value

load_dotenv()

MISTRAL_KEY = __require("MISTRAL_KEY", os.getenv("MISTRAL_KEY"))

