import logging

from config.config import LLM_CLIENT, URGENCY_CLASSIFIER, URGENCY_SCALERS
from fastapi import Depends, Request
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from prompts.prompt_manager import JinjaPromptManager
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from workflows.components.response_synthesiser import ResponseSynthesiserComponent
from workflows.components.source_retrieval import SourceRetrievalComponent
from workflows.rag_workflow import RAGWorkflow

logger = logging.getLogger(__name__)


def get_llm_client(request: Request) -> ChatOpenAI | ChatGroq:
    """
    Gets the appropriate Langchain AzureChatOpenAI or ChatOpenAI Client.

    Returns:
        ChatOpenAI | ChatGroq: The Langchain ChatOpenAI or ChatGroq instance
    """
    return getattr(request.app.state, LLM_CLIENT)


def get_urgency_classifier(request: Request) -> LogisticRegression | RFE | GridSearchCV:
    """
    Gets the appropriate urgency classifier.

    Returns:
        LogisticRegression | RFE | GridSearchCV: The urgency classification instance.
    """
    return getattr(request.app.state, URGENCY_CLASSIFIER)


def get_urgency_scalers(request: Request) -> dict[str, MinMaxScaler]:
    """
    Gets the dictionary of MinMaxScalers fitted on training data.

    Returns:
        dict[str, MinMaxScaler]: Dictionary mapping numeric column names to respective MinMaxScaler.
    """
    return getattr(request.app.state, URGENCY_SCALERS)


def get_prompt_manager() -> JinjaPromptManager:
    """
    Gets the Jinja2 prompt manager.

    Returns:
        JinjaPromptManager: Prompt Manager to manage Jinja Prompts
    """
    return JinjaPromptManager()


def get_rag_workflow(
    llm_client: ChatOpenAI | ChatGroq = Depends(get_llm_client),
    prompt_manager: JinjaPromptManager = Depends(get_prompt_manager),
) -> RAGWorkflow:
    """
    Gets the RAG Pipeline.

    Args:
        llm_client (ChatOpenAI | ChatGroq): LLM Client depending on get_llm_client
        prompt_manager (JinjaPromptManager): Jinja Prompt Manager depending on get_prompt_manager

    Returns:
        RAGWorkflow: RAG Workflow object for general enquires.
    """
    # Set up components
    source_retrieval = SourceRetrievalComponent(
        name="faiss_index",
        num_sources=4,
    )
    response_synthesiser = ResponseSynthesiserComponent(
        llm_client=llm_client,
        prompt_manager=prompt_manager,
        prompt_filename="response_synthesis.yaml",
    )
    # Set up workflow
    rag_workflow = RAGWorkflow(
        source_retrieval=source_retrieval, response_synthesiser=response_synthesiser
    )
    # Build Graph and return
    rag_workflow.build_graph()
    return rag_workflow


def get_diagnosis_workflow(
    llm_client: ChatOpenAI | ChatGroq = Depends(get_llm_client),
    prompt_manager: JinjaPromptManager = Depends(get_prompt_manager),
) -> RAGWorkflow:
    """
    Gets the RAG Pipeline specifically for diagnosis workflow.

    Args:
        llm_client (ChatOpenAI | ChatGroq): LLM Client depending on get_llm_client
        prompt_manager (JinjaPromptManager): Jinja Prompt Manager depending on get_prompt_manager

    Returns:
        RAGWorkflow: RAG Workflow object for diagnosis.
    """
    # Set up components
    source_retrieval = SourceRetrievalComponent(
        name="faiss_index",
        num_sources=4,
    )
    response_synthesiser = ResponseSynthesiserComponent(
        llm_client=llm_client,
        prompt_manager=prompt_manager,
        prompt_filename="automated_diagnosis.yaml",
    )
    # Set up workflow
    diagnosis_workflow = RAGWorkflow(
        source_retrieval=source_retrieval, response_synthesiser=response_synthesiser
    )
    # Build Graph and return
    diagnosis_workflow.build_graph()
    return diagnosis_workflow
