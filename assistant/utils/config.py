'''This is a config file.
It contains the configuration for the assistant.
'''

# Standard library imports
import os

# Third-party imports
from dotenv import load_dotenv


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