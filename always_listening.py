from sara_assistant.core.voice_input import VoiceInput
from sara_assistant.core.voice_output import VoiceOutput
from sara_assistant.core.command_router import CommandRouter


def main():
    speaker = VoiceOutput()
    listener = VoiceInput()
    router = CommandRouter()

    speaker.speak("Always listening mode activated.")

    while True:
        try:
            command = listener.listen()
            if not command:
                continue

            print(f"Heard: {command}")

            if command in ["exit", "quit", "stop sara"]:
                speaker.speak("Always listening mode disabled.")
                break

            response = router.route(command)
            speaker.speak(response)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
            speaker.speak("System error occurred.")


if __name__ == "__main__":
    main()
