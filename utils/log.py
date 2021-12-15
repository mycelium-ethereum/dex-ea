import os
import logging
import settings
import subprocess
from logging.handlers import TimedRotatingFileHandler

def setup_custom_logger(name):
    """
    This function is used to create a logger with StreamHandler
    to output log messages >= debug level to stderr.

    Args:
        name (str): Creates logger with this name

    Returns:
        logging: returns created logger
    """
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(settings.CONSOLE_LOG_LEVEL)
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)
    logger.addHandler(handler)
    return logger

def setup_file_logger(logger):
    """
    This function is used to add a TimedRotatingFileHandler to the
    current logger.

    Args:
        logger (logging): Current logger
        account (str): Strategy name
    """
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    file_handler = TimedRotatingFileHandler('logs/dex_ea.log', when='M', interval=30, backupCount=5)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(settings.FILE_LOG_LEVEL)
    logger.addHandler(file_handler)