import logging
import os
from contextlib import asynccontextmanager

from api.routers import analytics, chat
from config.config import LLM_CLIENT
from core.factories import (
    make_llm_client,
    setup_langsmith_config,
)
from core.settings import Settings, get_settings
from database.mongodb import init_db
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
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

    # Storage in app state for future use
    setattr(app.state, LLM_CLIENT, llm_client)

    # Init DB here
    pymongo_client = await init_db(s)

    logger.info("✅ Application startup complete!")

    # Hand over control to FastAPI
    yield

    # Shutdown
    logger.info("🚀 Application shutdown: Closing clients...")

    # Close any active clients here
    await pymongo_client.close()

    logger.info("✅ Application shutdown complete!")


def extend_routers_prefix(
    routers: list[APIRouter], app: FastAPI, *, prefix: str = ""
) -> None:
    """
    Extends the prefix of each router's endpoint.

    Args:
        routers (list[APIRouter]): A list of FastAPI routers.
        app (FastAPI): The FastAPI application.
        prefix (str): The prefix to be added to each router's endpoint.
    """
    for router in routers:
        app.include_router(router, prefix=prefix)


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
    # Set up CORS middleware here
    # TODO: Restrict allowed origins here
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # Include any routers here
    app.include_router(router)
    routers = [chat.router, analytics.router]
    extend_routers_prefix(routers, app, prefix="/api")
    # Setup logging config here
    setup_loggers(app)
    return app


app = create_app()
