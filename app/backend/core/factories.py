import logging
import os
import pickle

from core.settings import Settings
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "models"))

logger = logging.getLogger(__name__)


def setup_langsmith_config(s: Settings) -> None:
    """
    Set up LangSmith Configuration.

    Args:
        s (Settings): The Pydantic Settings
    """
    # Check for necessary field (Langchain API Key)
    if not s.LANGCHAIN_API_KEY:
        raise ValueError("LANGCHAIN_API_KEY not set")
    # Set up Langchain
    os.environ["LANGCHAIN_API_KEY"] = s.LANGCHAIN_API_KEY
    # Set up Monitoring if tracing is set to True
    if s.LANGCHAIN_TRACING_V2 == "true":
        os.environ["LANGCHAIN_TRACING_V2"] = s.LANGCHAIN_TRACING_V2
        os.environ["LANGCHAIN_PROJECT"] = s.LANGCHAIN_PROJECT


def make_llm_client(s: Settings) -> ChatOpenAI | ChatGroq:
    """
    Returns the right LLM client for the chosen host.

    Args:
        s (Settings): The Pydantic settings

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


def make_urgency_classifier(s: Settings) -> LogisticRegression | RFE | GridSearchCV:
    """
    Returns the right urgency classifier.

    Args:
        s (Settings): The Pydantic settings

    Raises:
        ValueError: Raises exception if classifier not found or any issues setting up clients

    Returns:
        LogisticRegression | RFE | GridSearchCV: Urgency Classifier.
    """
    # Set parameters for extracting
    filename: str = f"patient_{s.URGENCY_CLASSIFIER_TYPE}.pkl"
    filepath: str = os.path.join(MODELS_DIR, filename)

    # Try loading model pickle file
    try:
        logger.info(
            "Setting up Urgency Classifier (Type: %s)", s.URGENCY_CLASSIFIER_TYPE
        )
        with open(filepath, "rb") as f:
            return pickle.load(f)
    except Exception as exc:
        raise ValueError(f"Unable to set up Classification Model: {exc}")


def make_urgency_classifier_scalars() -> dict[str, MinMaxScaler]:
    """
    Extracts the scalars for the urgency classifier.

    Raises:
        ValueError: Raises exception if scalars not found or any issues setting up scalars

    Returns:
        dict[str, MinMaxScaler]: Dictionary of MinMaxScalars for each numeric column
    """
    # Set parameters for extracting
    filename: str = "patient_scalers_dict.pkl"
    filepath: str = os.path.join(MODELS_DIR, filename)

    # Try loading model pickle file
    try:
        logger.info("Setting up Urgency Scalers")
        with open(filepath, "rb") as f:
            return pickle.load(f)
    except Exception as exc:
        raise ValueError(f"Unable to set up Classification Model: {exc}")
