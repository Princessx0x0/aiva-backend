"""Logging configuration for AIVA."""
import logging
import sys


def setup_logging(level: str = "INFO"):
    """
    Configure application logging.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Set specific loggers to different levels if needed
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
