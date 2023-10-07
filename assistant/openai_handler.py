'''
This module handles the communication with OpenAI's API.
'''

# Standard library imports
import io

# Third-party imports
import openai
import requests
from PIL.Image import open as pil_open

# Module or application-specific imports
from .utils import ErrorHandler

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