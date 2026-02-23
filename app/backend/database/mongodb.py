import logging
from typing import List

from beanie import init_beanie
from core.settings import Settings
from pymongo import AsyncMongoClient
from pymongo.errors import PyMongoError
from schemas.chat import ChatResponse

# Pre-defined fields
DOCUMENT_MODELS = [ChatResponse]

logger = logging.getLogger(__name__)


async def init_db(s: Settings):
    """
    Generates the PyMongo client and initialise the Beanie Client

    Args:
        s (Settings): The Pydantic settings.

    Raises:
        ValueError: Raises exception if MONGODB_URI has not been set or any issues setting up client

    Returns:
        AsyncMongoClient: The PyMongo client.
    """
    if not s.MONGODB_URI:
        raise ValueError(
            "Unable to set up PyMongo client: Please ensure that either MONGODB_URI has been set."
        )

    try:
        logger.info("Setting up PyMongo Client using MONGODB_URI")
        client = AsyncMongoClient(s.MONGODB_URI)
        await init_beanie(
            database=client.get_database(s.DB_NAME), document_models=DOCUMENT_MODELS
        )
        return client

    except PyMongoError as exc:
        raise ValueError(f"Unable to set up PyMongo client: {exc}")


async def get_conversation_history(
    session_id: str, limit: int = 5
) -> List[ChatResponse]:
    """
    Searches for the latest ChatResponse to contextualise requests

    Args:
        session_id (str): Session ID to search for
        limit (int): Number of responses to limit to. Default to 5

    Returns:
        List[ChatResponse]: List of Chat Responses, sorted by descending create date
    """
    return (
        await ChatResponse.find(ChatResponse.session_id == session_id)
        .sort("-create_datetime")
        .limit(limit)
        .to_list()
    )
