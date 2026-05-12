import os
from dotenv import load_dotenv

load_dotenv()


class SaraBrain:
    """OpenAI-backed brain with safe local fallback."""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def ask(self, prompt: str) -> str:
        if not self.api_key:
            return (
                "AI brain is not connected. Create a .env file and add OPENAI_API_KEY."
            )

        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are SARA, a concise desktop assistant. Give practical, direct answers."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
                max_tokens=250,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"AI brain error: {e}"
