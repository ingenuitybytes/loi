'''This is a error handler file.
It contains the error handler for the assistant.
'''

# Module or application-specific imports
from .logger import log


class ErrorHandler:
    @staticmethod
    def handle(e, custom_message=None):
        message = custom_message if custom_message else str(e)
        log.error(message)
        return message