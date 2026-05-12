import webbrowser
from sara_assistant.app_info import APP_WEBSITE, APP_VERSION


class SaraUpdater:
    @staticmethod
    def current_version() -> str:
        return APP_VERSION

    @staticmethod
    def check_for_updates() -> str:
        webbrowser.open(APP_WEBSITE)
        return "Opened official project page for updates. Auto-update service can be added in future releases."
