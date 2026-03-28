import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from rich.logging import RichHandler
from hn_scraper import settings


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # already configured

    logger.setLevel(settings.log_level.upper())

    # Console handler (rich)
    console = RichHandler(rich_tracebacks=True, show_path=False)
    console.setLevel(settings.log_level.upper())
    logger.addHandler(console)

    # File handler (rotating — max 5MB × 3 backups)
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    fh = RotatingFileHandler(
        log_dir / "scraper.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s — %(message)s"))
    logger.addHandler(fh)

    return logger