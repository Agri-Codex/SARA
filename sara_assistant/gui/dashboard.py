import customtkinter as ctk
from sara_assistant.core.command_router import CommandRouter
from sara_assistant.core.voice_output import VoiceOutput
from sara_assistant.core.voice_input import VoiceInput


class SaraDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SARA Assistant")
        self.geometry("900x700")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.router = CommandRouter()
        self.speaker = VoiceOutput()
        self.listener = VoiceInput()

        self.header = ctk.CTkLabel(self, text="SARA - Jarvis Lite", font=("Arial", 28, "bold"))
        self.header.pack(pady=20)

        self.output_box = ctk.CTkTextbox(self, width=800, height=380)
        self.output_box.pack(pady=15)

        self.entry = ctk.CTkEntry(self, width=600, placeholder_text="Enter command...")
        self.entry.pack(pady=10)

        self.run_button = ctk.CTkButton(self, text="Execute", command=self.execute_command)
        self.run_button.pack(pady=8)

        self.voice_button = ctk.CTkButton(self, text="Voice Command", command=self.voice_command)
        self.voice_button.pack(pady=8)

    def log(self, message: str):
        self.output_box.insert("end", message + "\n")
        self.output_box.see("end")

    def execute_command(self):
        command = self.entry.get().strip()
        if not command:
            return
        self.process_command(command)
        self.entry.delete(0, "end")

    def voice_command(self):
        self.log("Listening for voice command...")
        try:
            command = self.listener.listen()
            self.process_command(command)
        except Exception as e:
            self.log(f"Voice error: {e}")

    def process_command(self, command: str):
        self.log(f"You: {command}")
        response = self.router.route(command)
        self.log(f"SARA: {response}")
        self.speaker.speak(response)
