'''
This module is responsible for the speech recognition.
'''


# Third-party imports
import speech_recognition as sr

# Module or application-specific imports
from .utils import ErrorHandler, log


class SpeechRecognizer:
    def recognize(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            log.info("Sprechen Sie einen Befehl")
            audio = r.listen(source)
        try:
            command = r.recognize_google(audio, language="de-DE")
            log.info("Erkannter Befehl: " + command)
            return command
        except sr.UnknownValueError:
            log.info("Befehl konnte nicht erkannt werden")
            return ""
        except Exception as e:
            ErrorHandler.handle(e, "Ein Fehler bei der Spracherkennung trat auf")
            return ""