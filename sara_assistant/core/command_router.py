from sara_assistant.automation.pc_control import PCControl

class CommandRouter:
    def route(self, command: str) -> str:
        command = command.lower()

        if "open google" in command:
            return PCControl.open_google()
        elif "open youtube" in command:
            return PCControl.open_youtube()
        elif "shutdown" in command:
            return PCControl.shutdown_pc()
        elif "hello" in command:
            return "Hello, I am SARA. How can I help you?"
        else:
            return f"Command not recognized: {command}"
