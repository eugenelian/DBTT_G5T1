import logging
import os

logger = logging.getLogger(__name__)


def create_folder(paths: list[str]) -> None:
    """
    Helper function to detect missing folders and create them

    Args:
        paths (list[str]): List of paths to create directories
    """
    logger.info("Creating folders at %s", str(paths))

    for path in paths:
        try:
            os.makedirs(path, exist_ok=True)
            logger.info(f"Ensured directory '{path}' exists")
        except OSError as exc:
            logger.warning("Exception faced when creating folder '%s': %s", path, exc)

    logger.info("Created all folders")
