import os
import webbrowser


class PCControl:
    @staticmethod
    def open_google():
        webbrowser.open("https://www.google.com")
        return "Opening Google"

    @staticmethod
    def open_youtube():
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube"

    @staticmethod
    def open_whatsapp_web():
        webbrowser.open("https://web.whatsapp.com")
        return "Opening WhatsApp Web"

    @staticmethod
    def open_notepad():
        os.system("start notepad")
        return "Opening Notepad"

    @staticmethod
    def shutdown_pc():
        return "Shutdown blocked until you say: confirm shutdown"

    @staticmethod
    def confirm_shutdown():
        os.system("shutdown /s /t 5")
        return "Confirmed. Shutting down PC in 5 seconds"
