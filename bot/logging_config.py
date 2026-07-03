"""
Logging configuration for the trading bot.
Sets up a logger that writes to both console and a log file.
"""

import logging
import os
from datetime import datetime

LOG_DIR = "logs"


def setup_logger(name: str = "trading_bot") -> logging.Logger:
    """
    Create and configure a logger.

    - Logs to a timestamped file inside logs/
    - Logs to console as well (INFO and above)
    - File captures everything at DEBUG level (requests, responses, errors)
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    log_filename = os.path.join(
        LOG_DIR, f"trading_bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Avoid adding duplicate handlers if setup_logger is called multiple times
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler: captures everything, useful for debugging/audit
    file_handler = logging.FileHandler(log_filename, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console handler: only show INFO and above, keep it clean for the user
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger