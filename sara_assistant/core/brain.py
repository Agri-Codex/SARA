import os


class SaraBrain:
    """Simple AI brain layer.

    If OPENAI_API_KEY is available, this can be extended to call an LLM.
    For now it safely returns a local response instead of breaking the app.
    """

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")

    def ask(self, prompt: str) -> str:
        if not self.api_key:
            return (
                "AI brain is not connected yet. Add OPENAI_API_KEY in your environment "
                "or .env file to enable ChatGPT responses."
            )
        return "OpenAI key detected. Live LLM call will be added in the next upgrade."
