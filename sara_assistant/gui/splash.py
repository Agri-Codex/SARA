import customtkinter as ctk
from sara_assistant.app_info import APP_NAME, APP_VERSION


class SplashScreen(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title(APP_NAME)
        self.geometry("640x420")
        self.overrideredirect(True)

        ctk.CTkLabel(self, text=APP_NAME, font=("Segoe UI", 34, "bold")).pack(pady=80)
        ctk.CTkLabel(self, text=f"Version {APP_VERSION}", font=("Segoe UI", 16)).pack(pady=10)
        ctk.CTkLabel(self, text="Initializing premium systems...", font=("Segoe UI", 14)).pack(pady=25)

        self.after(2200, self.destroy)
