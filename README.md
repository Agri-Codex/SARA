# OpenJarvisLite

## Sara — Open Source Local Assistant

Sara is a lightweight open-source assistant inspired by Jarvis. She is designed to run locally, speak with a friendly female persona, and optionally access the internet for search and updated information. Sara is also an expert in cyber security and ethical hacking.

### Features

- Local assistant mode with open-source model support
- Optional web search via DuckDuckGo
- Beautiful modern GUI with voice recognition and text-to-speech
- Command-line interface for advanced users
- Cyber security expertise and ethical hacking tools
- Password strength checker
- Basic port scanning
- Website security analysis
- Knowledge base for common security concepts
- Works offline and online

### Setup

1. Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run Sara:

```bash
# Web GUI (recommended - works everywhere)
python sara_web.py

# Desktop GUI (requires display)
python sara_gui.py

# Or CLI mode
python sara.py
```

### Usage

#### Web GUI Mode (Recommended)

Launch the web-based GUI that works in any environment:

```bash
python sara_web.py
```

Then open http://localhost:5000 in your browser.

Features:
- **Voice Input**: Click the voice button to speak your commands
- **Text Input**: Type messages in the input field
- **Web Search Toggle**: Enable/disable internet search
- **Real-time Chat**: Modern web interface with animations
- **Works Everywhere**: Browser-based, no desktop required

#### Desktop GUI Mode

Launch the desktop GUI (requires display environment):

```bash
python sara_gui.py
```

#### CLI Mode

Start the command-line interface:

```bash
python sara.py
```

Options:
- `--web`: Launch web GUI
- `--gui`: Launch desktop GUI
- `--no-web`: Disable internet search for offline mode
- `--search`: Force web search for every query
- `--model`: Specify local model (default: gpt2)

### Cyber Security Features

Sara includes built-in cyber security tools:

- **Password Strength Check**: `check password strength for mypassword123`
- **Port Scanning**: `scan ports for example.com`
- **Website Security**: `check website security for https://example.com`
- **Security Knowledge**: Ask about phishing, encryption, firewalls, VPNs, etc.
- **Nmap Integration**: `run nmap scan on target` (if nmap is installed)

### Examples

```bash
# General questions
Sara> Hello Sara
Sara> What is the weather today?

# Cyber security
Sara> Explain phishing attacks
Sara> Check password strength for P@ssw0rd123
Sara> Scan ports for localhost

# Web search
Sara> Search for latest cybersecurity news
```

### Project structure

- `sara/assistant.py` — core assistant logic
- `sara/search.py` — internet search and summary helpers
- `sara/cyber.py` — cyber security tools and knowledge
- `sara/gui.py` — modern GUI with voice/text input
- `sara/cli.py` — command-line interface
- `sara.py` — CLI entry point
- `sara_gui.py` — GUI entry point
- `requirements.txt` — Python dependencies

### Requirements

- Python 3.8+
- For voice features: microphone access
- For advanced scanning: nmap (optional)
- Internet connection for web search

### Voice Setup

For voice recognition to work:
1. Install PortAudio: `sudo apt-get install portaudio19-dev` (Linux)
2. Ensure microphone permissions are granted
3. Test with: `python -c "import speech_recognition as sr; print('Voice ready')"`

### Ethical Use

Sara is designed for ethical hacking and learning. All tools are for educational and defensive purposes only. Always obtain permission before scanning networks or systems.

---

Sara is ready to grow into a more advanced open-source horizon AI assistant. Feel free to extend her memory, add plugins, or connect a browser automation layer later.
