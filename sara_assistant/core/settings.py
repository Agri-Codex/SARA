import json
from pathlib import Path
from sara_assistant.config import DATA_DIR

SETTINGS_FILE = DATA_DIR / "settings.json"

DEFAULT_SETTINGS = {
    "theme": "premium_dark",
    "voice_enabled": True,
    "speak_responses": True,
    "openai_model": "gpt-4o-mini",
    "launch_on_startup": False,
    "onboarding_complete": False,
    "active_profile": "Default User"
}


class SettingsManager:
    def __init__(self):
        DATA_DIR.mkdir(exist_ok=True)
        if not SETTINGS_FILE.exists():
            self.save(DEFAULT_SETTINGS)

    def load(self):
        try:
            return json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
        except Exception:
            self.save(DEFAULT_SETTINGS)
            return DEFAULT_SETTINGS.copy()

    def save(self, settings: dict):
        SETTINGS_FILE.write_text(json.dumps(settings, indent=2), encoding="utf-8")

    def set_value(self, key: str, value):
        settings = self.load()
        settings[key] = value
        self.save(settings)
        return settings
