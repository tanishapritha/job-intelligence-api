import logging
from config import LOG_LEVEL

LOG_LEVEL_MAP = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARN": logging.WARNING,
    "ERROR": logging.ERROR,
}

level = LOG_LEVEL_MAP.get(LOG_LEVEL.upper(), logging.INFO)
logging.basicConfig(
    level=level,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)
logger = logging.getLogger("job_intel")
