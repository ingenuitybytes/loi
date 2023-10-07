#!/usr/bin/env python3
'''This is the logger file.
It contains the logger configuration.
'''

import logging
import logging.handlers
import colorlog


def setup_logger():
    LOG_LEVEL = logging.INFO
    LOGFORMAT_CONSOLE = '%(log_color)s%(levelname)-10s%(reset)s[%(asctime)s] %(name)s: %(message)s'
    LOGFORMAT_FILE = '%(levelname)-10s[%(asctime)s] %(name)s: %(message)s'
    DATEFORMAT = '%d/%b/%Y %H:%M:%S'

    # Setze Logging-Level für discord und discord.http
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)

    # console handler
    stream = logging.StreamHandler()
    formatter_console = colorlog.ColoredFormatter(
        LOGFORMAT_CONSOLE, 
        datefmt=DATEFORMAT,
        log_colors={
            'DEBUG': 'white',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    stream.setFormatter(formatter_console)
    logger.addHandler(stream)

    # file handler
    file_handler = logging.handlers.RotatingFileHandler(
        filename='console.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5
    )
    formatter_file = logging.Formatter(LOGFORMAT_FILE, DATEFORMAT)
    file_handler.setFormatter(formatter_file)
    logger.addHandler(file_handler)
    
    return logger

log = setup_logger()
