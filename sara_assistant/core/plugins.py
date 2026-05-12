import json
from sara_assistant.config import DATA_DIR

PLUGIN_FILE = DATA_DIR / "plugins.json"

DEFAULT_PLUGINS = [
    {"name": "Browser Automation", "enabled": True},
    {"name": "WhatsApp Web", "enabled": True},
    {"name": "Memory System", "enabled": True},
    {"name": "OpenAI Brain", "enabled": True},
]


class PluginMarketplace:
    def __init__(self):
        DATA_DIR.mkdir(exist_ok=True)
        if not PLUGIN_FILE.exists():
            self.save(DEFAULT_PLUGINS)

    def load(self):
        return json.loads(PLUGIN_FILE.read_text(encoding="utf-8"))

    def save(self, plugins):
        PLUGIN_FILE.write_text(json.dumps(plugins, indent=2), encoding="utf-8")

    def list_plugins(self):
        plugins = self.load()
        return "Available plugins: " + ", ".join([p["name"] for p in plugins])
