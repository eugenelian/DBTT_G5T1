import logging

from core.dependencies import get_rag_workflow
from fastapi import APIRouter, Depends, status
from schemas.chat import ChatRequest
from workflows import RAGWorkflow

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/chat", tags=["Chat"])


@router.post(
    "",
    # response_model=ChatResponseV2,
    status_code=status.HTTP_200_OK,
    summary="Chat",
)
async def chat(
    request_data: ChatRequest,
    rag_workflow: RAGWorkflow = Depends(get_rag_workflow),
):
    # TODO: Retrieve Chat History here

    # Run the pipeline
    return await rag_workflow.run_pipeline(state=request_data.model_dump())
