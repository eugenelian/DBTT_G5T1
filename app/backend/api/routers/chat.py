import logging

from core.dependencies import get_rag_workflow
from database.mongodb import get_conversation_history
from fastapi import APIRouter, Depends, status
from schemas.chat import ChatRequest, ChatResponse
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
