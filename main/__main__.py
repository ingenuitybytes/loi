#!/usr/bin/env python3
'''This is the main file.
It starts the assistant.
'''

# Standard library imports
import os
import io
import signal  # Für sauberes Beenden

# Third-party imports
from dotenv import load_dotenv
import openai
import boto3
import speech_recognition as sr
from playsound import playsound
import requests
from PIL.Image import open as pil_open
import botocore.exceptions

# Module or application-specific imports
import utils


class Config:
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    @classmethod
    def check_required_configs(cls):
        # Überprüfen Sie nur Attribute, die nicht mit "__" beginnen.
        for attr, value in vars(cls).items():
            if not attr.startswith("__") and value is None:
                raise ValueError(f"Required configuration {attr} is missing!")
                exit(1)  # Beendet die Anwendung, wenn eine erforderliche Konfiguration fehlt.
class ErrorHandler:
    @staticmethod
    def handle(e, custom_message=None):
        message = custom_message if custom_message else str(e)
        utils.log.error(message)
        return message

class SpeechRecognizer:
    def recognize(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            utils.log.info("Sprechen Sie einen Befehl")
            audio = r.listen(source)
        try:
            command = r.recognize_google(audio, language="de-DE")
            utils.log.info("Erkannter Befehl: " + command)
            return command
        except sr.UnknownValueError:
            utils.log.info("Befehl konnte nicht erkannt werden")
            return ""
        except Exception as e:
            ErrorHandler.handle(e, "Ein Fehler bei der Spracherkennung trat auf")
            return ""
class TextToSpeech:
    def __init__(self, aws_access_key_id, aws_secret_access_key):
        self.polly = boto3.client(
            'polly',
            region_name='eu-central-1',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

    def synthesize(self, text):
        try:
            response = self.polly.synthesize_speech(Text=text,
                                                    OutputFormat='mp3',
                                                    VoiceId='Daniel',
                                                    Engine='neural',
                                                    LanguageCode='de-DE')
            audio_stream = response['AudioStream'].read()
            subfolder = "resources"
            if not os.path.exists(subfolder):
                os.makedirs(subfolder)
            file_path = os.path.join(subfolder, 'output.mp3')
            with open(file_path, 'wb') as file:
                file.write(audio_stream)
            playsound(file_path)
        except botocore.exceptions.BotoCoreError as e:
            ErrorHandler.handle(e, "Ein internes botocore Fehler trat auf")
        except botocore.exceptions.ClientError as e:
            ErrorHandler.handle(e, "Ein Client-Fehler trat auf")
class OpenAIHandler:
    def __init__(self, openai_api_key):
        openai.api_key = openai_api_key
        self.system_message = self._load_system_message()

    def _load_system_message(self):
        with open('resources/system_message.txt', 'r', encoding='utf-8') as file:
            return file.read().strip()

    def process_command(self, query):
        model_name = 'gpt-3.5-turbo'
        try:
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": self.system_message},
                    {"role": "user", "content": query}
                ],
                temperature=0.5
            )
            reply = response.choices[0].message.content
            if "[IMAGE_REQUEST]" in reply:
                picture_query = reply.replace("[IMAGE_REQUEST]", "").strip()
                image_url = self._generate_image(picture_query)
                self._display_image(image_url)
                return "Das Bild wurde generiert!"
            else:
                return reply
        except requests.exceptions.RequestException as e:
            ErrorHandler.handle(e, "Netzwerkfehler beim Kontaktieren von OpenAI")
            return "Entschuldigung, es gab ein Problem bei der Kommunikation mit OpenAI."

    def _generate_image(self, picture_query):
        try:
            response = openai.Image.create(
                prompt=picture_query,
                n=1,
                size="1024x1024"
            )
            image_url = response['data'][0]['url']
            return image_url
        except requests.exceptions.RequestException as e:
            ErrorHandler.handle(e, "Netzwerkfehler beim Erzeugen eines Bildes")
            return None

    def _display_image(self, image_url):
        try:
            response = requests.get(image_url)
            image = pil_open(io.BytesIO(response.content))
            image.show()
        except requests.exceptions.RequestException as e:
            ErrorHandler.handle(e, "Netzwerkfehler beim Abrufen eines Bildes")

class Assistant:
    def __init__(self):
        Config.check_required_configs()
        self._initialize_resources_folder()
        self.speech_recognizer = SpeechRecognizer()
        self.text_to_speech = TextToSpeech(Config.AWS_ACCESS_KEY_ID, Config.AWS_SECRET_ACCESS_KEY)
        self.openai_handler = OpenAIHandler(Config.OPENAI_API_KEY)

    def _initialize_resources_folder(self):
        subfolder = "resources"
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)

    def _graceful_exit(self, signum, frame):
        utils.log.info("Der Assistant wurde sauber beendet!")
        exit(0)

    def run(self):
        # Signalhandler für sauberes Beenden hinzufügen
        signal.signal(signal.SIGINT, self._graceful_exit)
        
        while True:
            try:
                command = self.speech_recognizer.recognize()
                if command:
                    response = self.openai_handler.process_command(command)
                    self.text_to_speech.synthesize(response)
            except Exception as e:
                ErrorHandler.handle(e, "Ein kritischer Fehler trat auf")

if __name__ == "__main__":
    assistant = Assistant()
    assistant.run()
