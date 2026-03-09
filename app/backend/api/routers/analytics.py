import logging

from data.data_manager import get_patient_data
from fastapi import APIRouter, Depends, status
from pandas import DataFrame
from schemas.patient_analytics import PatientsAnalyticsResponse

from utils.patient_analytics import get_patient_analytics

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/analytics", tags=["Analytics"])


@router.get(
    "",
    response_model=PatientsAnalyticsResponse,
    status_code=status.HTTP_200_OK,
    summary="Analytics",
)
async def analytics(
    patient_df: DataFrame = Depends(get_patient_data),
):
    # Obtain analytics
    return get_patient_analytics(df=patient_df)
