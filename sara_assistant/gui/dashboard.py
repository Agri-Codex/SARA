import random
import customtkinter as ctk
from sara_assistant.core.command_router import CommandRouter
from sara_assistant.core.voice_output import VoiceOutput
from sara_assistant.core.voice_input import VoiceInput
from sara_assistant.core.settings import SettingsManager
from sara_assistant.core.cyber_tools import CyberToolRegistry
from sara_assistant.app_info import APP_NAME, APP_VERSION
from sara_assistant import ui_theme as theme
from sara_assistant.gui.components import AnimatedAvatar, VoiceWaveform, NotificationCenter
from sara_assistant.gui.settings_window import SettingsWindow
from sara_assistant.gui.onboarding import OnboardingWizard
from sara_assistant.gui.splash import SplashScreen


class SaraDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry("1520x900")
        self.configure(fg_color=theme.APP_BG)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.settings = SettingsManager()
        self.router = CommandRouter()
        self.speaker = VoiceOutput()
        self.listener = VoiceInput()

        self.show_splash()
        self.build_layout()
        self.run_first_launch_onboarding()

    def show_splash(self):
        try:
            splash = SplashScreen(self)
            splash.after(2200, splash.destroy)
        except Exception:
            pass

    def run_first_launch_onboarding(self):
        settings = self.settings.load()
        if not settings.get("onboarding_complete", False):
            self.after(900, lambda: OnboardingWizard(self))

    def build_layout(self):
        self.sidebar = ctk.CTkFrame(self, width=270, fg_color=theme.PANEL_BG, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.brand = ctk.CTkLabel(self.sidebar, text="SARA PREMIUM", font=theme.FONT_TITLE, text_color=theme.ACCENT)
        self.brand.pack(pady=(28, 6))

        self.version = ctk.CTkLabel(self.sidebar, text=f"Version {APP_VERSION}", font=theme.FONT_SUBTITLE, text_color=theme.TEXT_MUTED)
        self.version.pack(pady=(0, 18))

        self.avatar = AnimatedAvatar(self.sidebar)
        self.avatar.pack(pady=12, padx=20, fill="x")

        self.waveform = VoiceWaveform(self.sidebar)
        self.waveform.pack(pady=(4, 18), padx=22)

        quick_commands = [
            ("Open Google", "open google"),
            ("Open YouTube", "open youtube"),
            ("Open WhatsApp", "open whatsapp"),
            ("Open Notepad", "open notepad"),
            ("Recall Memory", "recall memory"),
            ("Check Updates", "check updates"),
        ]

        for label, cmd in quick_commands:
            ctk.CTkButton(self.sidebar, text=label, command=lambda c=cmd: self.process_command(c), fg_color=theme.ACCENT_DARK, hover_color=theme.ACCENT, font=theme.FONT_BUTTON, corner_radius=12, height=40).pack(pady=5, padx=20, fill="x")

        ctk.CTkButton(self.sidebar, text="Settings", command=self.open_settings, fg_color=theme.CARD_BG, hover_color=theme.ACCENT_DARK, font=theme.FONT_BUTTON, corner_radius=12, height=40).pack(pady=(18, 6), padx=20, fill="x")
        ctk.CTkButton(self.sidebar, text="Onboarding", command=lambda: OnboardingWizard(self), fg_color=theme.CARD_BG, hover_color=theme.ACCENT_DARK, font=theme.FONT_BUTTON, corner_radius=12, height=40).pack(pady=5, padx=20, fill="x")

        self.status = ctk.CTkLabel(self.sidebar, text="System Status: Online", text_color=theme.SUCCESS, font=theme.FONT_BODY)
        self.status.pack(side="bottom", pady=22)

        self.main_panel = ctk.CTkFrame(self, fg_color=theme.APP_BG)
        self.main_panel.pack(side="left", fill="both", expand=True)

        self.header = ctk.CTkLabel(self.main_panel, text="Premium AI + Cybersecurity Command Center", font=theme.FONT_TITLE, text_color=theme.TEXT_MAIN)
        self.header.pack(pady=(24, 6))

        self.subheader = ctk.CTkLabel(self.main_panel, text="Voice • Automation • Memory • AI • Plugins • Security • Cyber Tools", font=theme.FONT_SUBTITLE, text_color=theme.TEXT_MUTED)
        self.subheader.pack(pady=(0, 16))

        self.output_box = ctk.CTkTextbox(self.main_panel, width=820, height=430, fg_color=theme.CARD_BG, text_color=theme.TEXT_MAIN, corner_radius=18, font=theme.FONT_BODY)
        self.output_box.pack(pady=10)

        self.cyber_box = ctk.CTkTextbox(self.main_panel, width=820, height=170, fg_color=theme.CARD_BG, text_color=theme.TEXT_MAIN, corner_radius=18, font=theme.FONT_BODY)
        self.cyber_box.pack(pady=8)
        self.cyber_box.insert("end", CyberToolRegistry.list_tools_text() + "\n\n" + CyberToolRegistry.safety_notice())

        self.entry = ctk.CTkEntry(self.main_panel, width=740, height=48, placeholder_text="Enter command or ask AI...", corner_radius=14)
        self.entry.pack(pady=(14, 10))

        self.button_row = ctk.CTkFrame(self.main_panel, fg_color="transparent")
        self.button_row.pack(pady=8)

        ctk.CTkButton(self.button_row, text="Execute", command=self.execute_command, fg_color=theme.ACCENT_DARK, hover_color=theme.ACCENT, width=170, height=45, corner_radius=14).pack(side="left", padx=8)
        ctk.CTkButton(self.button_row, text="Voice Command", command=self.voice_command, fg_color=theme.SUCCESS, hover_color="#16A34A", width=170, height=45, corner_radius=14).pack(side="left", padx=8)
        ctk.CTkButton(self.button_row, text="Clear", command=self.clear_log, fg_color=theme.DANGER, hover_color="#B91C1C", width=130, height=45, corner_radius=14).pack(side="left", padx=8)

        self.right_panel = ctk.CTkFrame(self, width=330, fg_color=theme.PANEL_BG, corner_radius=0)
        self.right_panel.pack(side="right", fill="y")

        ctk.CTkLabel(self.right_panel, text="System Center", font=("Segoe UI", 22, "bold"), text_color=theme.TEXT_MAIN).pack(pady=(28, 12))
        self.notification_center = NotificationCenter(self.right_panel)
        self.notification_center.pack(padx=16, pady=12, fill="x")
        self.notification_center.notify("Premium UI loaded.")
        self.notification_center.notify("Cybersecurity toolkit panel loaded.")

        self.info_box = ctk.CTkTextbox(self.right_panel, width=290, height=260, fg_color=theme.CARD_BG, text_color=theme.TEXT_MAIN, corner_radius=16)
        self.info_box.pack(padx=16, pady=12)
        self.info_box.insert("end", "Active Modules:\n• AI Brain\n• Memory\n• Voice Input\n• Security Vault\n• Plugin Marketplace\n• Mobile Sync Framework\n• Wake-word Framework\n• Cybersecurity Toolkit\n")

    def open_settings(self):
        SettingsWindow(self)
        self.notification_center.notify("Settings window opened.")

    def log(self, message: str):
        self.output_box.insert("end", message + "\n")
        self.output_box.see("end")

    def clear_log(self):
        self.output_box.delete("1.0", "end")
        self.notification_center.notify("Command log cleared.")

    def execute_command(self):
        command = self.entry.get().strip()
        if not command:
            return
        self.process_command(command)
        self.entry.delete(0, "end")

    def voice_command(self):
        self.log("Listening for voice command...")
        self.waveform.animate_level(random.uniform(0.35, 0.95))
        self.notification_center.notify("Voice command mode activated.")
        try:
            command = self.listener.listen()
            self.waveform.animate_level(0.2)
            self.process_command(command)
        except Exception as e:
            self.waveform.animate_level(0.0)
            self.log(f"Voice error: {e}")
            self.notification_center.notify("Voice error detected.")

    def process_command(self, command: str):
        self.log(f"You: {command}")
        response = self.router.route(command)
        self.log(f"SARA: {response}")
        self.notification_center.notify(f"Command executed: {command[:28]}")
        self.speaker.speak(response)
