"""
Provide utils for logging.
"""

import logging

from src.settings import settings


def configure_logging():
    """
    Configure logging.
    """
    logging.basicConfig(level=settings.log_level)
