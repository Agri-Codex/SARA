import json
import webbrowser
from pathlib import Path

UPDATE_MANIFEST = Path("update_manifest.json")


class AutoUpdater:
    @staticmethod
    def local_manifest():
        if UPDATE_MANIFEST.exists():
            try:
                return json.loads(UPDATE_MANIFEST.read_text(encoding="utf-8"))
            except Exception:
                return None
        return None

    @staticmethod
    def check() -> str:
        manifest = AutoUpdater.local_manifest()
        if not manifest:
            return "No update manifest configured yet."
        return f"Latest available version: {manifest.get('latest_version', 'unknown')}"

    @staticmethod
    def open_release_page(url: str):
        webbrowser.open(url)
        return "Opened official release page."
