"""
Structured logging configuration using loguru.
"""
import sys
import os
from loguru import logger

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def setup_logging(level: str = LOG_LEVEL) -> None:
    logger.remove()
    logger.add(
        sys.stderr,
        level=level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
    )
    # File logging — skip on read-only filesystems (e.g. Vercel serverless)
    try:
        os.makedirs("logs", exist_ok=True)
        logger.add(
            "logs/app.log",
            level="DEBUG",
            rotation="10 MB",
            retention="7 days",
            compression="zip",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        )
    except (OSError, PermissionError):
        pass  # Read-only filesystem, skip file logging


setup_logging()

__all__ = ["logger"]
