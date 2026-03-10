import logging
import os

import numpy as np
import pandas as pd
from pandas import DataFrame

# Expose paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Files used in functions
PATIENT_DATA_FILENAME: str = "patient_priority_modified.csv"

logger = logging.getLogger(__name__)

# Chest Pain Mapping between types and name
CHEST_PAIN_MAP: dict[int, str] = {
    0: "Asymptomatic",
    1: "Atypical Angina",
    2: "Non-Anginal",
    3: "Typical Angina",
    4: "Severe Angina",
}


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
    file_path = os.path.abspath(os.path.join(SCRIPT_DIR, filename))
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Filename {filename} cannot be found.")

    # Extract as csv and return
    return pd.read_csv(file_path, index_col=False)


def get_patient_data() -> DataFrame | None:
    """
    Function to extract patient data from csv.

    Raises:
        ValueError: If any issues faced during getting patient data.

    Returns:
        DataFrame | None: Returns extracted DataFrame or None if not found.
    """
    try:
        # Extract DataFrame using utils function
        df = extract_df_from_csv(filename=PATIENT_DATA_FILENAME)

        # Modifies DataFrame to enhance data
        df["age_group"] = pd.cut(
            df["age"],
            bins=[0, 30, 40, 50, 60, 70, np.inf],
            labels=["<30", "30-40", "40-50", "50-60", "60-70", "70+"],
            right=False,
        )
        df["bp_category"] = pd.cut(
            df["blood pressure"],
            bins=[0, 120, 130, 140, np.inf],
            labels=[
                "Normal (<120)",
                "Elevated (120-129)",
                "Stage 1 (130-139)",
                "Stage 2 (≥140)",
            ],
            right=False,
        )
        df["bmi_category"] = pd.cut(
            df["bmi"],
            bins=[0, 18.5, 25, 30, np.inf],
            labels=["Underweight", "Normal", "Overweight", "Obese"],
            right=False,
        )
        df["chest_pain_label"] = (
            df["chest pain type"].map(CHEST_PAIN_MAP).fillna("Unknown")
        )

        # Returns DataFrame here
        return df

    except Exception as exc:
        raise ValueError(f"Error found in extracting DataFrame from csv: {exc}")
