import json
from sara_assistant.config import DATA_DIR

PROFILES_FILE = DATA_DIR / "profiles.json"


class ProfileManager:
    def __init__(self):
        DATA_DIR.mkdir(exist_ok=True)
        if not PROFILES_FILE.exists():
            self.save([{"name": "Default User", "role": "Owner"}])

    def load(self):
        return json.loads(PROFILES_FILE.read_text(encoding="utf-8"))

    def save(self, profiles):
        PROFILES_FILE.write_text(json.dumps(profiles, indent=2), encoding="utf-8")

    def add_profile(self, name: str, role: str = "User"):
        profiles = self.load()
        profiles.append({"name": name, "role": role})
        self.save(profiles)
        return profiles
