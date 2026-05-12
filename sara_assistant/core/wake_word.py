class WakeWordEngine:
    """Porcupine integration placeholder.

    Full production integration should connect pvporcupine + microphone loop.
    """

    @staticmethod
    def status() -> str:
        return (
            "Wake-word framework ready. Install pvporcupine and configure access key "
            "for production always-listening mode."
        )
