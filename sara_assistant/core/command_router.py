from sara_assistant.automation.pc_control import PCControl
from sara_assistant.core.brain import SaraBrain
from sara_assistant.core.memory import Memory
from sara_assistant.core.updater import SaraUpdater


class CommandRouter:
    def __init__(self):
        self.brain = SaraBrain()
        self.memory = Memory()

    def route(self, command: str) -> str:
        command = command.lower().strip()

        if "open google" in command:
            response = PCControl.open_google()
        elif "open youtube" in command:
            response = PCControl.open_youtube()
        elif "open whatsapp" in command:
            response = PCControl.open_whatsapp_web()
        elif "open notepad" in command:
            response = PCControl.open_notepad()
        elif "check updates" in command:
            response = SaraUpdater.check_for_updates()
        elif "version" in command:
            response = f"Current version: {SaraUpdater.current_version()}"
        elif command == "shutdown":
            response = PCControl.shutdown_pc()
        elif command == "confirm shutdown":
            response = PCControl.confirm_shutdown()
        elif command.startswith("remember "):
            response = self.memory.remember(command.replace("remember ", "", 1))
        elif "recall memory" in command:
            response = self.memory.recall()
        elif "hello" in command:
            response = "Hello, I am SARA. How can I help you?"
        else:
            response = self.brain.ask(command)

        self.memory.log_command(command, response)
        return response
