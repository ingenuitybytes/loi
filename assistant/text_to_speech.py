'''
This module is responsible for the text to speech conversion.
'''

# Standard library imports
import os


# Third-party imports
from dotenv import load_dotenv
import boto3
from playsound import playsound
import botocore.exceptions

# Module or application-specific imports
from .utils import ErrorHandler


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
            file_path = os.path.join("resources", 'temp.mp3')
            with open(file_path, 'wb') as file:
                file.write(audio_stream)
            playsound(file_path)
        except botocore.exceptions.BotoCoreError as e:
            ErrorHandler.handle(e, "Ein internes botocore Fehler trat auf")
        except botocore.exceptions.ClientError as e:
            ErrorHandler.handle(e, "Ein Client-Fehler trat auf")