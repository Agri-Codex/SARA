import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from sara_assistant.config import VOSK_MODEL_PATH

class VoiceInput:
    def __init__(self):
        if not VOSK_MODEL_PATH.exists():
            raise FileNotFoundError(f"Vosk model missing: {VOSK_MODEL_PATH}")
        self.model = Model(str(VOSK_MODEL_PATH))
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.audio_queue = queue.Queue()

    def _callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.audio_queue.put(bytes(indata))

    def listen(self):
        print("Listening...")
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16",
                               channels=1, callback=self._callback):
            while True:
                data = self.audio_queue.get()
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").strip()
                    if text:
                        return text
