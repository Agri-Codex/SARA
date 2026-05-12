"""Web-based GUI for Sara Assistant using Flask."""

import os
from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit
import threading

try:
    import speech_recognition as sr
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False

from .assistant import SaraAssistant

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sara - Cyber Security Assistant</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 90%;
            max-width: 800px;
            height: 90vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 20px 20px 0 0;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .chat-container {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f8f9fa;
        }
        .message {
            margin-bottom: 15px;
            padding: 12px 18px;
            border-radius: 18px;
            max-width: 70%;
            word-wrap: break-word;
            animation: fadeIn 0.3s ease-in;
        }
        .message.user {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin-left: auto;
            border-bottom-right-radius: 5px;
        }
        .message.sara {
            background: white;
            color: #333;
            border-bottom-left-radius: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .message.voice {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            margin-left: auto;
            border-bottom-right-radius: 5px;
        }
        .input-container {
            padding: 20px;
            background: white;
            border-radius: 0 0 20px 20px;
            border-top: 1px solid #e9ecef;
        }
        .input-group {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        #messageInput {
            flex: 1;
            padding: 12px 18px;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s;
        }
        #messageInput:focus {
            border-color: #667eea;
        }
        .btn {
            padding: 12px 20px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-block;
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .btn-success {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
        }
        .btn-success:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(79, 172, 254, 0.4);
        }
        .btn-danger {
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
            color: white;
        }
        .btn-danger:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 154, 158, 0.4);
        }
        .controls {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
            align-items: center;
        }
        .switch {
            position: relative;
            display: inline-block;
            width: 60px;
            height: 34px;
        }
        .switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }
        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: .4s;
            border-radius: 34px;
        }
        .slider:before {
            position: absolute;
            content: "";
            height: 26px;
            width: 26px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
        }
        input:checked + .slider {
            background-color: #667eea;
        }
        input:checked + .slider:before {
            transform: translateX(26px);
        }
        .status {
            font-size: 14px;
            color: #666;
            font-style: italic;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .typing {
            display: none;
            font-style: italic;
            color: #666;
            padding: 10px;
        }
        .typing.show {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Sara</h1>
            <p>Your Cyber Security Assistant</p>
        </div>

        <div class="chat-container" id="chatContainer">
            <div class="message sara">
                <strong>Sara:</strong> Hello! I'm Sara, your cyber security assistant. I can help with security questions, ethical hacking, and general assistance. How can I help you today?
            </div>
        </div>

        <div class="input-container">
            <div class="controls">
                <label class="switch">
                    <input type="checkbox" id="webSearchToggle" checked>
                    <span class="slider"></span>
                </label>
                <span>Web Search</span>
                <div class="status" id="status">Ready to assist...</div>
            </div>

            <div class="input-group">
                <input type="text" id="messageInput" placeholder="Type your message here..." autocomplete="off">
                <button class="btn btn-primary" id="sendButton">Send</button>
                <button class="btn btn-success" id="voiceButton">🎤 Voice</button>
            </div>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.2/socket.io.js"></script>
    <script>
        const socket = io();
        const chatContainer = document.getElementById('chatContainer');
        const messageInput = document.getElementById('messageInput');
        const sendButton = document.getElementById('sendButton');
        const voiceButton = document.getElementById('voiceButton');
        const webSearchToggle = document.getElementById('webSearchToggle');
        const statusDiv = document.getElementById('status');

        let isListening = false;

        // Send message
        function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;

            // Add user message
            addMessage('user', message);
            messageInput.value = '';

            // Send to server
            socket.emit('send_message', {
                message: message,
                search: webSearchToggle.checked
            });

            statusDiv.textContent = 'Thinking...';
        }

        // Voice input
        function toggleVoice() {
            if (isListening) {
                socket.emit('stop_voice');
                voiceButton.textContent = '🎤 Voice';
                voiceButton.className = 'btn btn-success';
                isListening = false;
            } else {
                socket.emit('start_voice');
                voiceButton.textContent = '⏹️ Stop';
                voiceButton.className = 'btn btn-danger';
                isListening = true;
                statusDiv.textContent = 'Listening...';
            }
        }

        // Add message to chat
        function addMessage(type, message, isVoice = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            if (isVoice) messageDiv.classList.add('voice');

            const sender = type === 'sara' ? 'Sara:' : 'You:';
            messageDiv.innerHTML = `<strong>${sender}</strong> ${message}`;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        // Event listeners
        sendButton.addEventListener('click', sendMessage);
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
        voiceButton.addEventListener('click', toggleVoice);

        // Socket events
        socket.on('sara_response', (data) => {
            addMessage('sara', data.message);
            statusDiv.textContent = 'Ready to assist...';
        });

        socket.on('voice_started', () => {
            statusDiv.textContent = 'Listening...';
        });

        socket.on('voice_stopped', () => {
            statusDiv.textContent = 'Voice input stopped';
        });

        socket.on('voice_result', (data) => {
            addMessage('user', data.message, true);
            statusDiv.textContent = 'Processing voice input...';
        });

        socket.on('error', (data) => {
            addMessage('sara', `Error: ${data.message}`);
            statusDiv.textContent = 'Error occurred';
        });
    </script>
</body>
</html>
"""

class SaraWebGUI:
    """Web-based GUI for Sara assistant."""

    def __init__(self):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.assistant = SaraAssistant()

        # Voice recognition
        self.voice_recognizer = sr.Recognizer() if VOICE_AVAILABLE else None
        self.tts_engine = pyttsx3.init() if VOICE_AVAILABLE else None
        self.is_listening = False

        if self.tts_engine:
            voices = self.tts_engine.getProperty('voices')
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower() or 'hazel' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            self.tts_engine.setProperty('rate', 180)

        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template_string(HTML_TEMPLATE)

        @self.socketio.on('send_message')
        def handle_message(data):
            message = data.get('message', '')
            search = data.get('search', False)

            try:
                response = self.assistant.answer(message, search=search)
                self.socketio.emit('sara_response', {'message': response})

                # Speak response
                if self.tts_engine:
                    threading.Thread(target=self.speak_text, args=(response,), daemon=True).start()

            except Exception as e:
                self.socketio.emit('error', {'message': str(e)})

        @self.socketio.on('start_voice')
        def start_voice():
            if not VOICE_AVAILABLE:
                self.socketio.emit('error', {'message': 'Voice recognition not available'})
                return

            self.is_listening = True
            self.socketio.emit('voice_started')
            threading.Thread(target=self.listen_for_speech, daemon=True).start()

        @self.socketio.on('stop_voice')
        def stop_voice():
            self.is_listening = False
            self.socketio.emit('voice_stopped')

    def listen_for_speech(self):
        """Listen for speech input."""
        try:
            with sr.Microphone() as source:
                self.voice_recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.voice_recognizer.listen(source, timeout=5, phrase_time_limit=10)

            text = self.voice_recognizer.recognize_google(audio)
            self.socketio.emit('voice_result', {'message': text})

            # Process the voice input
            response = self.assistant.answer(text, search=False)
            self.socketio.emit('sara_response', {'message': response})

            # Speak response
            if self.tts_engine:
                threading.Thread(target=self.speak_text, args=(response,), daemon=True).start()

        except sr.WaitTimeoutError:
            self.socketio.emit('error', {'message': 'No speech detected'})
        except sr.UnknownValueError:
            self.socketio.emit('error', {'message': 'Could not understand audio'})
        except sr.RequestError as e:
            self.socketio.emit('error', {'message': f'Speech service error: {e}'})
        except Exception as e:
            self.socketio.emit('error', {'message': f'Voice error: {e}'})
        finally:
            self.is_listening = False

    def speak_text(self, text: str):
        """Speak text using TTS."""
        if self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"TTS error: {e}")

    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Run the web server."""
        print(f"Starting Sara Web GUI on http://{host}:{port}")
        print("Open this URL in your browser to use Sara!")
        self.socketio.run(self.app, host=host, port=port, debug=debug)


def main():
    """Launch the Sara Web GUI."""
    gui = SaraWebGUI()
    gui.run()


if __name__ == "__main__":
    main()