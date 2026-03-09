from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

SMOKING_STATUS = Literal[
    "formerly smoked",
    "never smoked",
    "smokes",
]


class TriageRequest(BaseModel):
    age: int = Field(..., description="Age of Patient")
    chest_pain_type: float = Field(
        ..., min=1.0, max=4.0, description="Chest Pain Type (1, 2, 3, 4)"
    )
    blood_pressure: int = Field(..., description="Systolic Blood Pressure of Patient")
    max_heart_rate: int = Field(..., description="Maximum Heart Rate of Patient")
    exercise_angina: int = Field(
        ..., description="Presence of Exercise Angina in Patient (0, 1)"
    )
    bmi: float = Field(..., description="BMI of Patient")
    hypertension: int = Field(
        ..., description="Presence of Hypertension in Patient (0, 1)"
    )
    heart_disease: int = Field(
        ..., description="Presence of Heart Disease in Patient (0, 1)"
    )
    smoking_status: SMOKING_STATUS = Field(..., description="Smoking Status of Patient")

    model_config = ConfigDict(extra="ignore")


class TriageResponse(BaseModel):
    urgency: int = Field(
        ..., description="Indicator on whether patient is urgent, 0 or 1."
    )
