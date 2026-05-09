import logging
from typing import Optional

try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, TextGenerationPipeline, pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

from .search import duckduckgo_search, summarize_search_results
from .cyber import CyberSecurityTools

DEFAULT_MODEL = "gpt2"


class SaraAssistant:
    """A lightweight assistant that can run locally and use web search when available."""

    def __init__(self, model_name: str = DEFAULT_MODEL, allow_internet: bool = True, use_local_model: bool = True):
        self.persona = (
            "Sara is a friendly female assistant with a horizon-focused voice. "
            "She is designed to work locally and optionally use internet search to answer questions. "
            "She is also an expert in cyber security and ethical hacking."
        )
        self.model_name = model_name
        self.allow_internet = allow_internet
        self.use_local_model = use_local_model
        self.model = None
        self.pipeline: Optional[TextGenerationPipeline] = None
        self.cyber_tools = CyberSecurityTools()
        self.memory = []
        self.load_local_model()

    def load_local_model(self):
        if not self.use_local_model:
            logging.info("Local model disabled.")
            return

        if not TRANSFORMERS_AVAILABLE:
            logging.warning("Transformers package is missing. Local model is unavailable.")
            return

        try:
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            model = AutoModelForCausalLM.from_pretrained(self.model_name)
            self.pipeline = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                device=-1,
            )
            self.model = model
            logging.info("Loaded local model %s", self.model_name)
        except Exception as exc:
            logging.warning("Unable to load local model '%s': %s", self.model_name, exc)
            self.pipeline = None

    def create_prompt(self, user_input: str) -> str:
        return (
            f"Sara is a kind, open-source assistant. {self.persona}\n"
            f"User: {user_input}\n"
            "Sara:"
        )

    def generate_response(self, user_input: str) -> str:
        # Check for cyber security commands
        cyber_response = self.handle_cyber_command(user_input)
        if cyber_response:
            return cyber_response

        if self.pipeline:
            prompt = self.create_prompt(user_input)
            try:
                result = self.pipeline(
                    prompt,
                    max_new_tokens=120,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    pad_token_id=self.pipeline.tokenizer.eos_token_id,
                )
                text = result[0]["generated_text"]
                return text[len(prompt) :].strip()
            except Exception as exc:
                logging.warning("Local model generation failed: %s", exc)

        return self.simple_reply(user_input)

    def handle_cyber_command(self, user_input: str) -> Optional[str]:
        """Handle cyber security related commands."""
        lower_input = user_input.lower()

        if "password strength" in lower_input or "check password" in lower_input:
            # Extract password from input
            password = user_input.split("password")[-1].strip()
            if password:
                return self.cyber_tools.check_password_strength(password)
            return "Please provide a password to check its strength."

        if "scan ports" in lower_input or "port scan" in lower_input:
            # Extract target from input
            target = None
            if "for" in lower_input:
                target = lower_input.split("for")[-1].strip()
            elif "on" in lower_input:
                target = lower_input.split("on")[-1].strip()
            if target:
                return self.cyber_tools.scan_ports(target)
            return "Please specify a target IP or hostname to scan."

        if "nmap" in lower_input:
            target = user_input.split("nmap")[-1].strip()
            if target:
                return self.cyber_tools.run_nmap_scan(target)
            return "Please specify a target for nmap scan."

        if "website security" in lower_input or "check website" in lower_input:
            url = None
            if "for" in lower_input:
                url = lower_input.split("for")[-1].strip()
            if url and not url.startswith("http"):
                url = "https://" + url
            if url:
                return self.cyber_tools.check_website_security(url)
            return "Please specify a website URL to check."

        # General cyber security questions
        cyber_topics = ["phishing", "encryption", "firewall", "vpn", "two factor", "sql injection", "xss", "ddos", "malware"]
        for topic in cyber_topics:
            if topic in lower_input:
                return self.cyber_tools.get_security_info(topic)

        return None

    def simple_reply(self, user_input: str) -> str:
        lower = user_input.lower()
        if any(token in lower for token in ["hello", "hi", "hey"]):
            return "Hello! I'm Sara, your local assistant. Ask me anything, and I can also search the web if internet access is enabled. I'm also an expert in cyber security!"
        if "thank" in lower:
            return "You're welcome. I'm here to help."
        if "time" in lower:
            from datetime import datetime

            return f"The local time is {datetime.now().strftime('%H:%M:%S')} for your environment."
        if "internet" in lower or "search" in lower:
            return (
                "I can search the internet for you when web access is enabled. "
                "Type your question or use the search mode."
            )
        if "cyber" in lower or "security" in lower or "hacking" in lower:
            return (
                "I'm an expert in cyber security and ethical hacking. "
                "I can help with password strength checks, port scanning, website security analysis, and explain security concepts. "
                "What would you like to know?"
            )
        return (
            "Sara is ready to assist locally. "
            "If you want more up-to-date information, enable internet search with --no-web disabled."
        )

    def answer(self, user_input: str, search: bool = False) -> str:
        self.memory.append(user_input)
        if search and self.allow_internet:
            search_results = duckduckgo_search(user_input)
            summary = summarize_search_results(search_results)
            if summary:
                return f"I found some answers on the web:\n{summary}"
            return "I could not find a useful web summary, so here is my local answer:\n" + self.generate_response(user_input)

        return self.generate_response(user_input)
