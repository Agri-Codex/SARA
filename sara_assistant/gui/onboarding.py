import customtkinter as ctk
from sara_assistant.core.settings import SettingsManager


class OnboardingWizard(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.settings = SettingsManager()
        self.title("Welcome to SARA")
        self.geometry("720x520")

        ctk.CTkLabel(self, text="Welcome to SARA Premium", font=("Segoe UI", 28, "bold")).pack(pady=30)
        ctk.CTkLabel(
            self,
            text="Configure your assistant, API key, voice preferences, and profiles.\nThis wizard prepares SARA for first launch.",
            font=("Segoe UI", 14),
        ).pack(pady=20)

        self.finish_btn = ctk.CTkButton(self, text="Finish Setup", command=self.finish)
        self.finish_btn.pack(pady=40)

    def finish(self):
        self.settings.set_value("onboarding_complete", True)
        self.destroy()
