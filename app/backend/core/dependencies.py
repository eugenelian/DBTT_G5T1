from fastapi import Depends, Request
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from workflows.components.response_synthesiser import ResponseSynthesiserComponent
from prompts.prompt_manager import JinjaPromptManager
from workflows.rag_workflow import RAGWorkflow

from config.config import LLM_CLIENT


def get_llm_client(request: Request) -> ChatOpenAI | ChatGroq:
    """
    Gets the appropriate Langchain AzureChatOpenAI or ChatOpenAI Client.

    Returns:
        ChatOpenAI | ChatGroq: The Langchain ChatOpenAI or ChatGroq instance
    """
    return getattr(request.app.state, LLM_CLIENT)


def get_prompt_manager() -> JinjaPromptManager:
    """Gets the Jinja2 prompt manager."""
    return JinjaPromptManager()


def get_rag_workflow(
    prompt_manager: JinjaPromptManager = Depends(get_prompt_manager),
    llm_client: ChatOpenAI | ChatGroq = Depends(get_llm_client)
) -> RAGWorkflow:
    # Set up components
    response_synthesiser = ResponseSynthesiserComponent(
        prompt_manager=prompt_manager,
        prompt_filename="response_synthesis.yaml",
        llm_client=llm_client,
    )
    # Set up workflow
    rag_workflow = RAGWorkflow(
        response_synthesiser=response_synthesiser
    )
    # Build Graph and return
    rag_workflow.build_graph()
    return rag_workflow
