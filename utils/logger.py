#!/usr/bin/env python3
'''This is the logger file.
It contains the logger configuration.
'''

# Import modules and files
import logging
import colorlog


# Configure logging variables
LOG_LEVEL = logging.DEBUG
LOGFORMAT = '%(log_color)s%(levelname)-10s%(reset)s[%(asctime)s] %(name)s: %(message)s'
DATEFORMAT = '%d/%b/%Y %H:%M:%S'

# Logger erstellen
logger = colorlog.getLogger()
logger.setLevel(logging.INFO)

# Set formatter
formatter = colorlog.ColoredFormatter(LOGFORMAT, datefmt=DATEFORMAT,
    log_colors={
        'DEBUG': 'white',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
            'SUCCESS': 'green'
    })

handler = colorlog.StreamHandler()
handler.setFormatter(formatter)

logger.addHandler(handler)