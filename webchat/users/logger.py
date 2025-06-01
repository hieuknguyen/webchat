# logger.py
import logging

logger = logging.getLogger("webchat_logger")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(console_handler)
