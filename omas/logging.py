from pathlib import Path
from loguru import logger


def configure_logging(log_path: Path, level: str = "INFO") -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger.remove()
    logger.add(lambda m: print(m, end=""), level=level)
    logger.add(str(log_path), level=level, rotation="10 MB")
