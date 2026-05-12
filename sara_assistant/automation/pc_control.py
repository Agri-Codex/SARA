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
    def shutdown_pc():
        os.system("shutdown /s /t 5")
        return "Shutting down PC in 5 seconds"
