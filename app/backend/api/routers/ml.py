import logging

from core.dependencies import get_urgency_classifier_component
from fastapi import APIRouter, Depends, status
from pandas import DataFrame
from schemas.urgency_classification import TriageRequest, TriageResponse
from workflows.components.urgency_classifier import UrgencyClassfierComponent

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/ml", tags=["Machine Learning"])


@router.get(
    "/urgency",
    response_model=TriageResponse,
    status_code=status.HTTP_200_OK,
    summary="Urgency Classification",
)
async def urgency_classification(
    request_data: TriageRequest,
    component: UrgencyClassfierComponent = Depends(get_urgency_classifier_component),
):
    """
    ### Sample Hardcoded data

    request_data = TriageRequest(
        age=49.0,
        chest_pain_type=3.0,
        blood_pressure=160.0,
        max_heart_rate=156.0,
        exercise_angina=0,
        bmi=18.0,
        hypertension=0.0,
        heart_disease=0.0,
        smoking_status="never smoked",
    )
    """

    # Preprocess data
    X: DataFrame = component.prepare_data(request_data=request_data)
    print(X.iloc[0])

    # Inference and return results
    return component.predict_single(X=X)
