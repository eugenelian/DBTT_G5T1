import logging
import os

from core.settings import Settings
from langchain.tools import BaseTool
from langchain_community.tools import ArxivQueryRun
from langchain_community.utilities import ArxivAPIWrapper
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)


def make_llm_client(s: Settings) -> ChatOpenAI | ChatGroq:
    """
    Returns the right LLM client for the chosen host.

    Args:
        s (Settings): The Pydantic settings.

    Raises:
        ValueError: Raises exception if both OPENAI_API_KEY and GROQ_API_KEY have not been set or any issues setting up clients

    Returns:
        ChatOpenAI | ChatGroq: The LLM client. Returns OpenAI client by default
    """
    try:
        if s.LLM_MODEL == "OPENAI_MODEL" and s.OPENAI_API_KEY:
            logger.info(
                "Setting up OpenAI LLM (%s) using OPENAI_API_KEY", s.OPENAI_MODEL
            )
            return ChatOpenAI(api_key=s.OPENAI_API_KEY, model=s.OPENAI_MODEL)
        elif s.LLM_MODEL == "GROQ_MODEL" and s.GROQ_API_KEY:
            logger.info("Setting up Groq LLM (%s) using GROQ_API_KEY", s.GROQ_MODEL)
            return ChatGroq(api_key=s.GROQ_API_KEY, model=s.GROQ_MODEL)
        # If no OPENAI_API_KEY or GROQ_API_KEY, raise ValueError
        raise ValueError(
            "Unable to set up LLM client: Please ensure that either OPENAI_API_KEY or GROQ_API_KEY has been set."
        )
    except Exception as exc:
        raise ValueError(f"Unable to set up LLM client: {exc}")


def setup_langsmith_config(s: Settings) -> None:
    # Check for necessary field (Langchain API Key)
    if not s.LANGCHAIN_API_KEY:
        raise ValueError("LANGCHAIN_API_KEY not set")
    # Set up Langchain
    os.environ["LANGCHAIN_API_KEY"] = s.LANGCHAIN_API_KEY
    # Set up Monitoring if tracing is set to True
    if s.LANGCHAIN_TRACING_V2 == "true":
        os.environ["LANGCHAIN_TRACING_V2"] = s.LANGCHAIN_TRACING_V2
        os.environ["LANGCHAIN_PROJECT"] = s.LANGCHAIN_PROJECT


def setup_tools(s: Settings) -> list[BaseTool]:
    """
    Returns list of tools that can be used by the LLM Agent.

    Args:
        s (Settings): The Pydantic settings.

    Returns:
        list[BaseTool]: List of tools that can be used by LLM Agent
    """
    tools = []
    # Declaring Arxiv API Wrapper and Query Run Tool
    if s.USE_ARXIV == "true":
        api_wrapper_arxiv = ArxivAPIWrapper(top_k_results=3, doc_content_chars_max=500)
        arxiv = ArxivQueryRun(api_wrapper=api_wrapper_arxiv)
        tools.append(arxiv)
    return tools
