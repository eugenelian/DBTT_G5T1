import logging

from beanie import init_beanie
from pymongo import AsyncMongoClient

from schemas.chat import ChatResponse
from core.settings import Settings

# Pre-defined fields
DOCUMENT_MODELS = [
    ChatResponse
]

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
        logger.info(
            "Setting up PyMongo Client using MONGODB_URI"
        )
        client = AsyncMongoClient(s.MONGODB_URI)
        await init_beanie(database=client.get_database(s.DB_NAME), document_models=DOCUMENT_MODELS)
        return client
    except Exception as exc:
        raise ValueError(f"Unable to set up PyMongo client: {exc}")
