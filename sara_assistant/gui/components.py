import customtkinter as ctk


class NotificationCenter(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.text = ctk.CTkTextbox(self, width=320, height=180)
        self.text.pack(fill="both", expand=True)

    def notify(self, message: str):
        self.text.insert("end", f"• {message}\n")
        self.text.see("end")


class AnimatedAvatar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.label = ctk.CTkLabel(self, text="◉ SARA", font=("Segoe UI", 26, "bold"))
        self.label.pack(padx=10, pady=10)


class VoiceWaveform(ctk.CTkProgressBar):
    def __init__(self, master):
        super().__init__(master, width=260)
        self.set(0.0)

    def animate_level(self, level: float):
        safe_level = max(0.0, min(1.0, level))
        self.set(safe_level)
