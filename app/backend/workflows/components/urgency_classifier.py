import logging

import pandas as pd
from pandas import DataFrame
from schemas.urgency_classification import TriageRequest
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler

logger = logging.getLogger(__name__)


# Set numeric_cols, binary_cols and categorical_cols
NUMERIC_COLS = ["age", "blood pressure", "max heart rate", "bmi"]
BINARY_COLS = ["exercise angina", "hypertension", "heart_disease"]
CATEGORICAL_COLS = ["chest pain type", "smoking_status"]
ALL_COLS = NUMERIC_COLS + BINARY_COLS + CATEGORICAL_COLS

# Set columns to rename
RENAME_COLS = {
    "chest_pain_type": "chest pain type",
    "blood_pressure": "blood pressure",
    "max_heart_rate": "max heart rate",
    "exercise_angina": "exercise angina",
}

# Set fixed categories
FIXED_CATEGORIES = {
    "chest pain type": [1.0, 2.0, 3.0, 4.0],
    "smoking_status": ["formerly smoked", "never smoked", "smokes"],
}


class UrgencyClassifierComponent:
    """
    The urgency classifier component classifies urgency based on the triage request data.
    """

    def __init__(
        self,
        urgency_classifier: LogisticRegression | RFE | GridSearchCV,
        urgency_scalers: dict[str, MinMaxScaler],
    ):
        self.urgency_classifier = urgency_classifier
        self.urgency_scalers = urgency_scalers

    def preprocess_data(
        self,
        X: DataFrame,
    ) -> DataFrame:
        """
        Function to preprocess data from X. This step should be performed after train-test split to not have data leakage.

        Args:
            X (DataFrame): DataFrame to be preprocessed.

        Returns:
            DataFrame: Preprocessed DataFrame
        """

        # Numeric Columns are normalised using MinMaxScaler to constrain values between 0 and 1
        for col in NUMERIC_COLS:
            scaler = self.urgency_scalers.get(col)
            if not scaler:
                logger.warning(
                    "Scaler for column '%s' not found. Skipping scaling.", col
                )
                continue
            # For val/test datasets, we use the existing scaler from scalers dict provided
            X[col] = self.urgency_scalers.get(col).transform(X[[col]])

        logger.debug("Successfully processed numeric column(s)")

        # Binary columns are converted to int
        for col in BINARY_COLS:
            X[col] = X[col].astype(int)

        logger.debug("Successfully processed binary column(s)")

        # Categorical columns are encoded through converting the column into dummy encoding using get_dummies() (from pandas).
        for col in CATEGORICAL_COLS:
            dummies = pd.get_dummies(X[col], prefix=col, dtype=int)

            # Reindex columns to fixed categories
            fixed_cols = [f"{col}_{cat}" for cat in FIXED_CATEGORIES[col]]
            dummies = dummies.reindex(columns=fixed_cols, fill_value=0)

            # Drop original column and concatenate dummies
            X = X.drop(columns=col)
            X = pd.concat([X, dummies], axis=1)

        logger.debug("Successfully processed categorical column(s)")

        return X

    def prepare_data(self, request_data: TriageRequest) -> DataFrame:
        """
        Formats data to DataFrame and perform preprocessing stage.

        Args:
            request_data (TriageRequest): Triage Request to preprocess data.

        Returns:
            DataFrame
        """
        # Convert Pydantic Object to DataFrame
        df = DataFrame(request_data.model_dump(), index=[0])

        # Rename columns
        df = df.rename(columns=RENAME_COLS)

        # Perform Preprocessing
        return self.preprocess_data(df)

    def predict_single(self, X: DataFrame) -> int:
        """
        Predicts the urgency based on a single row DataFrame.

        Args:
            X (DataFrame): DataFrame containing a single row of features

        Returns:
            int: Integer containing whether to return
        """
        urgency = self.urgency_classifier.predict(X)
        return urgency[0]
