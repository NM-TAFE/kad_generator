import logging
from logging.handlers import TimedRotatingFileHandler
import sys

logging.basicConfig(
    level=logging.DEBUG,  # Set the default logging level for the root logger
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Set the format for log messages
    handlers=[
        logging.StreamHandler(),  # Console handler
        TimedRotatingFileHandler(  # File handler
            filename="app.log", when="midnight", backupCount=7, encoding="utf-8"
        ),
    ],
)

log = logging.getLogger()
