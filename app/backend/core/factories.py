import os
import logging

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

from core.settings import Settings

logger = logging.getLogger(__name__)

def make_llm_client(s: Settings):
    if s.OPENAI_API_KEY:
        logger.info("Setting up OpenAI LLM (%s) using OPENAI_API_KEY", s.OPENAI_MODEL)
        return ChatOpenAI(api_key=s.OPENAI_API_KEY, model=s.OPENAI_MODEL)
    elif s.GROQ_API_KEY:
        logger.info("Setting up Groq LLM (%s) using GROQ_API_KEY", s.GROQ_MODEL)
        return ChatGroq(api_key=s.GROQ_API_KEY, model=s.GROQ_MODEL)
    return None


def setup_langsmith_config(s: Settings):
    # Check for necessary field (Langchain API Key)
    if not s.LANGCHAIN_API_KEY:
        raise ValueError("LANGCHAIN_API_KEY not set")
    # Set up Langchain
    os.environ["LANGCHAIN_API_KEY"] = s.LANGCHAIN_API_KEY
    # Set up Monitoring if tracing is set to True
    if s.LANGCHAIN_TRACING_V2 == "true":
        os.environ["LANGCHAIN_TRACING_V2"] = s.LANGCHAIN_TRACING_V2
        os.environ["LANGCHAIN_PROJECT"] = s.LANGCHAIN_PROJECT

