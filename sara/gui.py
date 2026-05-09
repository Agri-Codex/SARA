"""Graphical User Interface for Sara Assistant."""

import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

try:
    import customtkinter as ctk
    CUSTOM_TK_AVAILABLE = True
except ImportError:
    CUSTOM_TK_AVAILABLE = False
    import tkinter.ttk as ttk

try:
    import speech_recognition as sr
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False

from .assistant import SaraAssistant


class SaraGUI:
    """Modern GUI for Sara assistant with voice and text input."""

    def __init__(self):
        self.assistant = SaraAssistant()
        self.voice_recognizer = sr.Recognizer() if VOICE_AVAILABLE else None
        self.tts_engine = pyttsx3.init() if VOICE_AVAILABLE else None

        # Configure TTS
        if self.tts_engine:
            voices = self.tts_engine.getProperty('voices')
            # Try to set female voice
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower() or 'hazel' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            self.tts_engine.setProperty('rate', 180)

        # Setup GUI
        if CUSTOM_TK_AVAILABLE:
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")
            self.root = ctk.CTk()
        else:
            self.root = tk.Tk()

        self.root.title("Sara - Open Source Assistant")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        self.setup_ui()
        self.is_listening = False

    def setup_ui(self):
        """Setup the user interface."""
        if CUSTOM_TK_AVAILABLE:
            self.setup_customtk_ui()
        else:
            self.setup_tk_ui()

    def setup_customtk_ui(self):
        """Setup UI with CustomTkinter."""
        # Main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="Sara - Your Cyber Security Assistant",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10))

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            font=("Arial", 12),
            bg="#2b2b2b",
            fg="#ffffff",
            insertbackground="#ffffff"
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.chat_display.config(state=tk.DISABLED)

        # Input frame
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Text input
        self.text_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="Type your message here...",
            font=ctk.CTkFont(size=14)
        )
        self.text_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 5), pady=10)
        self.text_input.bind("<Return>", lambda e: self.send_message())

        # Buttons frame
        buttons_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        buttons_frame.pack(side=tk.RIGHT, padx=(0, 10), pady=10)

        # Send button
        self.send_button = ctk.CTkButton(
            buttons_frame,
            text="Send",
            command=self.send_message,
            width=80
        )
        self.send_button.pack(side=tk.LEFT, padx=(0, 5))

        # Voice button
        if VOICE_AVAILABLE:
            self.voice_button = ctk.CTkButton(
                buttons_frame,
                text="🎤 Voice",
                command=self.toggle_voice_input,
                width=80,
                fg_color="#28a745"
            )
            self.voice_button.pack(side=tk.LEFT, padx=(0, 5))

        # Search toggle
        self.search_var = tk.BooleanVar(value=self.assistant.allow_internet)
        self.search_switch = ctk.CTkSwitch(
            buttons_frame,
            text="Web Search",
            variable=self.search_var,
            onvalue=True,
            offvalue=False
        )
        self.search_switch.pack(side=tk.LEFT)

        # Status bar
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Ready to assist...",
            font=ctk.CTkFont(size=10)
        )
        self.status_label.pack(pady=(0, 10))

        # Welcome message
        self.add_message("Sara", "Hello! I'm Sara, your cyber security assistant. I can help with security questions, ethical hacking, and general assistance. How can I help you today?")

    def setup_tk_ui(self):
        """Setup UI with regular Tkinter."""
        # Configure dark theme
        self.root.configure(bg="#2b2b2b")
        style = ttk.Style()
        style.configure("TFrame", background="#2b2b2b")
        style.configure("TLabel", background="#2b2b2b", foreground="#ffffff", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 10))

        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="Sara - Your Cyber Security Assistant",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(20, 10))

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            font=("Arial", 12),
            bg="#1e1e1e",
            fg="#ffffff",
            insertbackground="#ffffff"
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.chat_display.config(state=tk.DISABLED)

        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Text input
        self.text_input = ttk.Entry(
            input_frame,
            font=("Arial", 14)
        )
        self.text_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 5), pady=10)
        self.text_input.bind("<Return>", lambda e: self.send_message())
        self.text_input.insert(0, "Type your message here...")

        # Buttons frame
        buttons_frame = ttk.Frame(input_frame)
        buttons_frame.pack(side=tk.RIGHT, padx=(0, 10), pady=10)

        # Send button
        self.send_button = ttk.Button(
            buttons_frame,
            text="Send",
            command=self.send_message
        )
        self.send_button.pack(side=tk.LEFT, padx=(0, 5))

        # Voice button
        if VOICE_AVAILABLE:
            self.voice_button = ttk.Button(
                buttons_frame,
                text="🎤 Voice",
                command=self.toggle_voice_input
            )
            self.voice_button.pack(side=tk.LEFT, padx=(0, 5))

        # Search toggle
        self.search_var = tk.BooleanVar(value=self.assistant.allow_internet)
        self.search_check = ttk.Checkbutton(
            buttons_frame,
            text="Web Search",
            variable=self.search_var
        )
        self.search_check.pack(side=tk.LEFT)

        # Status bar
        self.status_label = ttk.Label(
            main_frame,
            text="Ready to assist...",
            font=("Arial", 10)
        )
        self.status_label.pack(pady=(0, 10))

        # Welcome message
        self.add_message("Sara", "Hello! I'm Sara, your cyber security assistant. I can help with security questions, ethical hacking, and general assistance. How can I help you today?")

    def add_message(self, sender: str, message: str):
        """Add a message to the chat display."""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

        # Speak the message if it's from Sara
        if sender == "Sara" and self.tts_engine:
            threading.Thread(target=self.speak_text, args=(message,), daemon=True).start()

    def send_message(self):
        """Send a text message."""
        message = self.text_input.get().strip()
        if not message or message == "Type your message here...":
            return

        self.text_input.delete(0, tk.END)
        if not CUSTOM_TK_AVAILABLE:
            self.text_input.insert(0, "Type your message here...")
        self.add_message("You", message)
        self.status_label.configure(text="Thinking...")

        # Process in background
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()

    def process_message(self, message: str):
        """Process the message and get response."""
        try:
            search = self.search_var.get()
            response = self.assistant.answer(message, search=search)
            self.root.after(0, lambda: self.add_message("Sara", response))
            self.root.after(0, lambda: self.status_label.configure(text="Ready to assist..."))
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            self.root.after(0, lambda: self.add_message("Sara", error_msg))
            self.root.after(0, lambda: self.status_label.configure(text="Error occurred"))

    def toggle_voice_input(self):
        """Toggle voice input listening."""
        if not VOICE_AVAILABLE:
            messagebox.showerror("Error", "Voice recognition is not available. Please install speech_recognition and pyaudio.")
            return

        if self.is_listening:
            self.is_listening = False
            if CUSTOM_TK_AVAILABLE:
                self.voice_button.configure(text="🎤 Voice", fg_color="#28a745")
            else:
                self.voice_button.configure(text="🎤 Voice")
            self.status_label.configure(text="Voice input stopped")
        else:
            self.is_listening = True
            if CUSTOM_TK_AVAILABLE:
                self.voice_button.configure(text="⏹️ Stop", fg_color="#dc3545")
            else:
                self.voice_button.configure(text="⏹️ Stop")
            self.status_label.configure(text="Listening...")
            threading.Thread(target=self.listen_for_speech, daemon=True).start()

    def listen_for_speech(self):
        """Listen for speech input."""
        try:
            with sr.Microphone() as source:
                self.voice_recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.voice_recognizer.listen(source, timeout=5, phrase_time_limit=10)

            text = self.voice_recognizer.recognize_google(audio)
            self.root.after(0, lambda: self.add_message("You (voice)", text))
            self.root.after(0, lambda: self.status_label.configure(text="Processing voice input..."))

            # Process the voice input
            threading.Thread(target=self.process_message, args=(text,), daemon=True).start()

        except sr.WaitTimeoutError:
            self.root.after(0, lambda: self.status_label.configure(text="No speech detected"))
        except sr.UnknownValueError:
            self.root.after(0, lambda: self.status_label.configure(text="Could not understand audio"))
        except sr.RequestError as e:
            self.root.after(0, lambda: self.status_label.configure(text=f"Speech service error: {e}"))
        except Exception as e:
            self.root.after(0, lambda: self.status_label.configure(text=f"Voice error: {e}"))
        finally:
            self.is_listening = False
            self.root.after(0, lambda: self.voice_button.configure(text="🎤 Voice", fg_color="#28a745"))

    def speak_text(self, text: str):
        """Speak text using TTS."""
        if self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"TTS error: {e}")

    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


def main():
    """Launch the Sara GUI."""
    gui = SaraGUI()
    gui.run()


if __name__ == "__main__":
    main()