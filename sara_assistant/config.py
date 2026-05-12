"""Configuration for SARA Phase 1."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

ASSISTANT_NAME = "SARA"
WAKE_WORD = "hey sara"

# Download a Vosk model and place it here:
# models/vosk-model-small-en-us-0.15
VOSK_MODEL_PATH = MODELS_DIR / "vosk-model-small-en-us-0.15"

MEMORY_FILE = DATA_DIR / "memory.json"

# Optional Picovoice Porcupine access key. Leave blank to use text wake fallback.
PORCUPINE_ACCESS_KEY = ""
PORCUPINE_KEYWORD = "hey siri"
