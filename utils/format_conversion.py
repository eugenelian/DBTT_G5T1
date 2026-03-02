import logging
import os
from typing import OrderedDict

import pyreadr
from file_management import create_folder
from pandas import DataFrame

# Set up logger
logger = logging.getLogger(__name__)

# Set up default data path
UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(UTILS_DIR, "..", "data"))

# Ensure data_dir exists
create_folder(paths=[DATA_DIR])


def convert_rdata_to_csv(
    file_name: str, dir_path: str = None, save_file_path: str = None
) -> None:
    """
    Converts an rdata datafile to csv format for easier processing.

    Args:
        file_name (str): Name of .rdata file to be converted.
        dir_path (str): Path of directory to find the file from. Defaults to '/data' directory.
        save_file_path (str): Path to save directory to. Defaults to the same directory as the input file with a .csv extension.
    """
    # Check for wrong datatype
    if not file_name.endswith(".rdata"):
        raise ValueError(
            f"Filename '{file_name}' of wrong file type received. Only accepts .rdata files."
        )

    # Replace dir_path if not provided
    if not dir_path:
        dir_path = DATA_DIR

    # Retrieve file path
    file_path = os.path.abspath(os.path.join(dir_path, file_name))
    logger.info("Reading .rdata file from %s", file_path)
    result: OrderedDict = pyreadr.read_r(file_path)

    # See objects inside
    logger.info("Objects in the result: %s", list(result.keys()))

    # Get the df object
    df: DataFrame = result.get("df")
    if df is None:
        raise ValueError("Key 'df' not present in file, please use a valid key.")

    # Save to CSV
    csv_file_path = (
        save_file_path if save_file_path else os.path.splitext(file_path)[0] + ".csv"
    )
    df.to_csv(csv_file_path, index=False)
    logger.info("Successfully saved csv to: %s", csv_file_path)


if __name__ == "__main__":
    # Settign up logger config
    logging.basicConfig(level=logging.INFO, format="%(name)s:\t%(message)s")

    # Set up configurations
    file_name = "5v_cleandf.rdata"
    save_file_name = "Hospital_Triage_and_Patient_History_Data.csv"
    save_file_path = os.path.abspath(os.path.join(DATA_DIR, save_file_name))

    # Convert file
    convert_rdata_to_csv(
        file_name=file_name, dir_path=DATA_DIR, save_file_path=save_file_path
    )
