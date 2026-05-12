import argparse
import sys

from .assistant import SaraAssistant


def parse_args():
    parser = argparse.ArgumentParser(
        description="Sara: an open-source local assistant with optional internet search."
    )
    parser.add_argument(
        "--model",
        default="gpt2",
        help="Local model name or path for transformers (default: gpt2).",
    )
    parser.add_argument(
        "--no-web",
        action="store_true",
        help="Disable internet search and keep Sara fully local.",
    )
    parser.add_argument(
        "--search",
        action="store_true",
        help="Force Sara to use internet search for every query when web access is enabled.",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch the graphical user interface instead of CLI.",
    )
    parser.add_argument(
        "--web",
        action="store_true",
        help="Launch the web-based GUI (works in any environment).",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.web:
        try:
            from .web_gui import SaraWebGUI
        except ImportError:
            print("Web GUI dependencies are missing. Install Flask and Flask-SocketIO to use --web.")
            return

        gui = SaraWebGUI()
        gui.run()
        return

    if args.gui:
        try:
            from .gui import SaraGUI
        except ImportError:
            print("Desktop GUI dependencies are missing or unavailable.")
            return

        gui = SaraGUI()
        gui.run()
        return

    assistant = SaraAssistant(
        model_name=args.model,
        allow_internet=not args.no_web,
        use_local_model=True,
    )

    print("\nSara is ready. Type a question, or type 'exit' to quit.")
    print("Use --no-web for offline mode or press Enter after each prompt.\n")

    while True:
        try:
            prompt = input("Sara> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye from Sara.")
            sys.exit(0)

        if not prompt:
            continue
        if prompt.lower() in {"exit", "quit", "bye", "stop"}:
            print("Goodbye from Sara.")
            break

        enable_search = args.search or ("search" in prompt.lower() or "internet" in prompt.lower())
        if enable_search and not assistant.allow_internet:
            print("Internet search is disabled. Run with no --no-web to enable web access.")
            response = assistant.answer(prompt, search=False)
        else:
            response = assistant.answer(prompt, search=enable_search)

        print(response)
