import customtkinter as ctk
from sara_assistant.core.settings import SettingsManager
from sara_assistant.core.plugins import PluginMarketplace
from sara_assistant.core.security import SecurityManager
from sara_assistant.core.mobile_sync import MobileSync


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.settings = SettingsManager()
        self.plugins = PluginMarketplace()

        self.title("SARA Settings")
        self.geometry("980x760")

        ctk.CTkLabel(self, text="SARA Settings Center", font=("Segoe UI", 28, "bold")).pack(pady=20)

        settings = self.settings.load()

        ctk.CTkLabel(self, text=f"Active Profile: {settings['active_profile']}").pack(pady=6)
        ctk.CTkLabel(self, text=f"Theme: {settings['theme']}").pack(pady=6)
        ctk.CTkLabel(self, text=f"Voice Enabled: {settings['voice_enabled']}").pack(pady=6)
        ctk.CTkLabel(self, text=f"Startup Launch: {settings['launch_on_startup']}").pack(pady=6)

        ctk.CTkTextbox(self, width=820, height=120).pack(pady=15)

        plugin_box = ctk.CTkTextbox(self, width=820, height=120)
        plugin_box.pack(pady=15)
        plugin_box.insert("end", self.plugins.list_plugins())

        security_box = ctk.CTkTextbox(self, width=820, height=120)
        security_box.pack(pady=15)
        security_box.insert("end", SecurityManager.security_report())

        sync_box = ctk.CTkTextbox(self, width=820, height=80)
        sync_box.pack(pady=15)
        sync_box.insert("end", MobileSync.sync_status())
