import logging

from core.dependencies import get_urgency_classifier_component
from fastapi import APIRouter, Depends, status
from pandas import DataFrame
from schemas.urgency_classification import TriageRequest, TriageResponse
from workflows.components.urgency_classifier import UrgencyClassifierComponent

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/ml", tags=["Machine Learning"])


@router.post(
    "/urgency",
    response_model=TriageResponse,
    status_code=status.HTTP_200_OK,
    summary="Urgency Classification",
)
async def urgency_classification(
    request_data: TriageRequest,
    component: UrgencyClassifierComponent = Depends(get_urgency_classifier_component),
):
    """
    ### Sample Hardcoded data

    request_data = TriageRequest(
        age=49,
        chest_pain_type=3.0,
        blood_pressure=160,
        max_heart_rate=156,
        exercise_angina=0,
        bmi=18.0,
        hypertension=0,
        heart_disease=0,
        smoking_status="never smoked"
    )
    """

    # Preprocess data
    X: DataFrame = component.prepare_data(request_data=request_data)

    # Predict
    urgency = component.predict_single(X=X)

    # Construct TriageResponse object and return
    return TriageResponse(**request_data.model_dump(), urgency=urgency)
