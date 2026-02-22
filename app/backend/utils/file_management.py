import logging
import os

logger = logging.getLogger(__name__)


def create_folder(paths: list[str]):
    """
    Helper function to detect missing folders and create them

    Args:
        paths (str): List of paths to create directories
    """
    logger.info("Creating folders at %s", str(paths))

    for path in paths:
        try:
            # Creates a new directory if path does not exists
            if not os.path.exists(path) or not os.path.isdir(path):
                logger.info(f"Directory '{path}' does not exist")
                if os.path.exists(path) and not os.path.isdir(path):
                    os.remove(path)  # Remove the file in the path
                os.mkdir(path)
                logger.info(f"Directory '{path}' created")
            # Returns path is it exists
            logger.info(f"Directory '{path}' exists")

        except Exception as exc:
            logger.warning("Exception faced when creating folder '%s': %s", path, exc)

    logger.info("Created all folders")
