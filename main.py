from sara_assistant.core.voice_input import VoiceInput
from sara_assistant.core.voice_output import VoiceOutput
from sara_assistant.core.command_router import CommandRouter


def main():
    speaker = VoiceOutput()
    listener = VoiceInput()
    router = CommandRouter()

    speaker.speak("SARA Phase One online.")

    while True:
        try:
            command = listener.listen()
            print(f"You said: {command}")

            if command in ["exit", "quit", "stop"]:
                speaker.speak("Shutting down. Goodbye.")
                break

            response = router.route(command)
            speaker.speak(response)

        except KeyboardInterrupt:
            speaker.speak("Manual shutdown detected.")
            break
        except Exception as e:
            print(f"Error: {e}")
            speaker.speak("An error occurred.")


if __name__ == "__main__":
    main()
