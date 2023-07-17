#!/usr/bin/env python3
'''This is the main file.
It starts the assistant.
'''

# Import modules and files
import os
from dotenv import load_dotenv
import openai
import boto3
import speech_recognition as sr
from playsound import playsound
import io
import requests
from PIL import Image

import utils


def load_api_keys():
    load_dotenv()

def process_command(query):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    model_name = 'gpt-3.5-turbo'
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "Du bist meine Künstliche Intelligenz namens Alpha. Ich habe dich erschaffen, um mir im Leben zu helfen."},
            {"role": "user", "content": query}
        ],
        temperature=0.5
    )
    reply = response.choices[0].message.content
    return reply

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        utils.logger.info("Sprechen Sie einen Befehl")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language="de-DE")
        utils.logger.info("Erkannter Befehl: " + command)
        return command

    except sr.UnknownValueError:
        utils.logger.info("Befehl konnte nicht erkannt werden")
        return ""
def speak(text):
    polly = boto3.client('polly',
                         region_name='eu-central-1',
                         aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                         aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
    response = polly.synthesize_speech(Text=text,
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

def generate_image(picture_query):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Image.create(
        prompt=picture_query,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url
def display_image(image_url):
    response = requests.get(image_url)
    image = Image.open(io.BytesIO(response.content))
    image.show()

if __name__ == "__main__":
    load_api_keys()
    while True:
        command = recognize_speech()
        if command:
            if "bild" in command.lower():
                image_url = generate_image(command)
                display_image(image_url)
                continue
            response = process_command(command)
            speak(response)