import logging
from uuid import uuid4

from core.dependencies import get_rag_workflow
from database.mongodb import get_conversation_history
from fastapi import APIRouter, Depends, status
from schemas.chat import ChatRequest, ChatResponse, DiagnosisRequest
from workflows import RAGWorkflow

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/chat", tags=["Chat"])


@router.post(
    "",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat",
)
async def chat(
    request_data: ChatRequest,
    rag_workflow: RAGWorkflow = Depends(get_rag_workflow),
):
    # Obtain conversation history
    conversation_history = await get_conversation_history(
        session_id=str(request_data.session_id)
    )

    # Run the pipeline
    return await rag_workflow.run_pipeline(
        state=request_data.model_dump(), conversation_history=conversation_history
    )


@router.post(
    "/diagnosis",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Automated Diagnosis",
)
async def diagnosis(
    request_data: DiagnosisRequest,
    rag_workflow: RAGWorkflow = Depends(get_rag_workflow),
):
    # Compile User Query
    user_query = f"Patient has the following symptoms: {request_data.symptoms}.\nDoctor Remarks: {request_data.remarks if request_data.remarks else "NIL"}\nWhat are some possible diagnosis?"

    # Extract out critical information from response model
    uuid_str: str = str(uuid4())
    data_dict: dict[str, str] = {
        "user_id": uuid_str,
        "session_id": uuid_str,
        "user_query": user_query,
    }

    # Run the pipeline
    return await rag_workflow.run_pipeline(state=data_dict, conversation_history=[])
