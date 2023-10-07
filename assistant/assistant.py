'''This is the main file.
It starts the assistant.
'''

# Standard library imports
import os
import signal  # Für sauberes Beenden

# Module or application-specific imports
from .utils import Config, ErrorHandler, log
from .speech_recognizer import SpeechRecognizer
from .text_to_speech import TextToSpeech
from .openai_handler import OpenAIHandler


class Assistant:
    def __init__(self):
        Config.check_required_configs()
        self._initialize_resources_folder()
        # Signalhandler für sauberes Beenden hinzufügen
        signal.signal(signal.SIGINT, self._graceful_exit)
        self.speech_recognizer = SpeechRecognizer()
        self.text_to_speech = TextToSpeech(Config.AWS_ACCESS_KEY_ID, Config.AWS_SECRET_ACCESS_KEY)
        self.openai_handler = OpenAIHandler(Config.OPENAI_API_KEY)

    def _initialize_resources_folder(self):
        subfolder = "resources"
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)

    def _graceful_exit(self, signum, frame):
        log.info("Der Assistant wurde sauber beendet!")
        exit(0)

    def run(self):
        while True:
            try:
                command = self.speech_recognizer.recognize()
                if command:
                    response = self.openai_handler.process_command(command)
                    self.text_to_speech.synthesize(response)
            except Exception as e:
                ErrorHandler.handle(e, "Ein kritischer Fehler trat auf")