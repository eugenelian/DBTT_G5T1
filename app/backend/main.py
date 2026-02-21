import logging
import os
from contextlib import asynccontextmanager

from core.factories import make_llm_client, setup_langsmith_config
from core.settings import Settings, get_settings
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, FastAPI, status
from fastapi.responses import JSONResponse
from rich.logging import RichHandler

logger = logging.getLogger(__name__)

# Load required env
load_dotenv()

# Instantiate FastAPI Router
router = APIRouter()


@router.get("/config")
def config(settings: Settings = Depends(get_settings)):
    return settings.get_shareable_config()


@router.get("/health")
def health_check():
    return JSONResponse(
        content={"status": "healthy", "message": "Health check passed!"},
        status_code=status.HTTP_200_OK,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Application startup: Initializing clients...")
    # Get Settings
    s = get_settings()

    # Set up any clients used here
    setup_langsmith_config(s)
    llm_client = make_llm_client(s)

    # Test LLM
    response = await llm_client.ainvoke("Hello!")
    logger.info("Response: %s", response)

    logger.info("✅ Application startup complete!")

    # Hand over control to FastAPI
    yield

    # Shutdown
    logger.info("🚀 Application shutdown: Closing clients...")

    # TODO: Close any active clients here

    logger.info("✅ Application shutdown complete!")


def setup_loggers(app: FastAPI) -> None:
    """
    Setup loggers for the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application.
    """
    # RichHandler does the colour & pretty formatting.
    FORMAT = "%(name)s:\t%(message)s"

    rich_handler = RichHandler(markup=True, rich_tracebacks=True)
    rich_handler.setFormatter(logging.Formatter(FORMAT))
    handlers = [rich_handler]

    logging.basicConfig(level=logging.INFO, format=FORMAT, handlers=handlers)
    app_level_str = os.getenv("APP_LOG_LEVEL", "INFO").upper()
    app_level = getattr(logging, app_level_str, logging.INFO)

    # Set our own logger levels (e.g., for this module, 'scripts' and 'agents')
    for name in [
        __name__,
        # Configure uvicorn's loggers if running with uvicorn directly
        "uvicorn.error",
        "uvicorn.access",
    ]:
        logging.getLogger(name).setLevel(app_level)


def create_app() -> FastAPI:
    # Instantiate application here
    app = FastAPI(title="DBTT G5T1", lifespan=lifespan, version="0.7.2")
    # TODO: Include any routers here
    app.include_router(router)
    # Setup logging config here
    setup_loggers(app)
    return app


app = create_app()
