import json
from datetime import datetime
from sara_assistant.config import MEMORY_FILE, DATA_DIR


class Memory:
    def __init__(self):
        DATA_DIR.mkdir(exist_ok=True)
        if not MEMORY_FILE.exists():
            MEMORY_FILE.write_text(json.dumps({"notes": [], "history": []}, indent=2), encoding="utf-8")

    def _load(self):
        return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))

    def _save(self, data):
        MEMORY_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def remember(self, text: str) -> str:
        data = self._load()
        data["notes"].append({"text": text, "time": datetime.now().isoformat(timespec="seconds")})
        self._save(data)
        return "I remembered that."

    def recall(self) -> str:
        data = self._load()
        notes = data.get("notes", [])[-5:]
        if not notes:
            return "I do not have any saved notes yet."
        return "Recent memory: " + " | ".join(note["text"] for note in notes)

    def log_command(self, command: str, response: str):
        data = self._load()
        data.setdefault("history", []).append({
            "command": command,
            "response": response,
            "time": datetime.now().isoformat(timespec="seconds"),
        })
        self._save(data)
