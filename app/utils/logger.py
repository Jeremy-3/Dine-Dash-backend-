# app/utils/logger.py
import logging

logger = logging.getLogger("APP")
logger.setLevel(logging.DEBUG)

# Prevent adding multiple handlers if the logger is imported multiple times
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s = %(name)s : %(levelname)s : %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
