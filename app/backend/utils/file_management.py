import logging
import os

import pandas as pd
from pandas import DataFrame

logger = logging.getLogger(__name__)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "data"))


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


def extract_df_from_csv(filename: str) -> DataFrame:
    """
    Helper function to extract a DataFrame from a filename

    Args:
        filename (str): Filename to extract DataFrame from.

    Raises:
        ValueError: If filename provided is not a csv.
        FileNotFoundError: If file cannot be found.

    Returns:
        DataFrame: DataFrame containing the data from the CSV file.
    """
    # Exception check for .csv extension
    if not filename.endswith(".csv"):
        raise ValueError(f"Filename {filename} must end with .csv.")

    # Obtain file path and check for existence
    file_path = os.path.abspath(os.path.join(DATA_DIR, filename))
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Filename {filename} cannot be found.")

    # Extract as csv and return
    return pd.read_csv(file_path, index_col=False)
