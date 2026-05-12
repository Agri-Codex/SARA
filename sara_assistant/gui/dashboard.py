import customtkinter as ctk
from sara_assistant.core.command_router import CommandRouter
from sara_assistant.core.voice_output import VoiceOutput
from sara_assistant.core.voice_input import VoiceInput
from sara_assistant.app_info import APP_NAME, APP_VERSION
from sara_assistant import ui_theme as theme


class SaraDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry("1280x820")
        self.configure(fg_color=theme.APP_BG)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.router = CommandRouter()
        self.speaker = VoiceOutput()
        self.listener = VoiceInput()

        self.build_layout()

    def build_layout(self):
        self.sidebar = ctk.CTkFrame(self, width=260, fg_color=theme.PANEL_BG, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.brand = ctk.CTkLabel(
            self.sidebar,
            text="SARA PREMIUM",
            font=theme.FONT_TITLE,
            text_color=theme.ACCENT,
        )
        self.brand.pack(pady=(30, 10))

        self.version = ctk.CTkLabel(
            self.sidebar,
            text=f"Version {APP_VERSION}",
            font=theme.FONT_SUBTITLE,
            text_color=theme.TEXT_MUTED,
        )
        self.version.pack(pady=(0, 25))

        quick_commands = [
            ("Open Google", "open google"),
            ("Open YouTube", "open youtube"),
            ("Open WhatsApp", "open whatsapp"),
            ("Open Notepad", "open notepad"),
            ("Recall Memory", "recall memory"),
            ("Check Updates", "check updates"),
        ]

        for label, cmd in quick_commands:
            ctk.CTkButton(
                self.sidebar,
                text=label,
                command=lambda c=cmd: self.process_command(c),
                fg_color=theme.ACCENT_DARK,
                hover_color=theme.ACCENT,
                font=theme.FONT_BUTTON,
                corner_radius=12,
                height=42,
            ).pack(pady=6, padx=20, fill="x")

        self.status = ctk.CTkLabel(
            self.sidebar,
            text="System Status: Online",
            text_color=theme.SUCCESS,
            font=theme.FONT_BODY,
        )
        self.status.pack(side="bottom", pady=25)

        self.main_panel = ctk.CTkFrame(self, fg_color=theme.APP_BG)
        self.main_panel.pack(side="right", fill="both", expand=True)

        self.header = ctk.CTkLabel(
            self.main_panel,
            text="Premium AI Command Center",
            font=theme.FONT_TITLE,
            text_color=theme.TEXT_MAIN,
        )
        self.header.pack(pady=(25, 10))

        self.subheader = ctk.CTkLabel(
            self.main_panel,
            text="Voice • Automation • Memory • AI",
            font=theme.FONT_SUBTITLE,
            text_color=theme.TEXT_MUTED,
        )
        self.subheader.pack(pady=(0, 20))

        self.output_box = ctk.CTkTextbox(
            self.main_panel,
            width=900,
            height=430,
            fg_color=theme.CARD_BG,
            text_color=theme.TEXT_MAIN,
            corner_radius=18,
            font=theme.FONT_BODY,
        )
        self.output_box.pack(pady=10)

        self.entry = ctk.CTkEntry(
            self.main_panel,
            width=720,
            height=48,
            placeholder_text="Enter command or ask AI...",
            corner_radius=14,
        )
        self.entry.pack(pady=(15, 10))

        self.button_row = ctk.CTkFrame(self.main_panel, fg_color="transparent")
        self.button_row.pack(pady=10)

        self.run_button = ctk.CTkButton(
            self.button_row,
            text="Execute",
            command=self.execute_command,
            fg_color=theme.ACCENT_DARK,
            hover_color=theme.ACCENT,
            width=170,
            height=45,
            corner_radius=14,
        )
        self.run_button.pack(side="left", padx=10)

        self.voice_button = ctk.CTkButton(
            self.button_row,
            text="Voice Command",
            command=self.voice_command,
            fg_color=theme.SUCCESS,
            hover_color="#16A34A",
            width=170,
            height=45,
            corner_radius=14,
        )
        self.voice_button.pack(side="left", padx=10)

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
