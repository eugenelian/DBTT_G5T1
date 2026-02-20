import logging
from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends, FastAPI, status
from fastapi.responses import JSONResponse

from core.settings import Settings, get_settings

# Instantiate Logger
logger = logging.getLogger(__name__)

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
    # s = get_settings()

    # TODO: Startup any database connections here

    logger.info("✅ Application startup complete!")

    # Hand over control to FastAPI
    yield

    # Shutdown
    logger.info("🚀 Application shutdown: Closing clients...")

    # TODO: Close any active clients here

    logger.info("✅ Application shutdown complete!")


def create_app() -> FastAPI:
    # Instantiate application here
    app = FastAPI(title="DBTT G5T1", lifespan=lifespan, version="0.7.2")
    # TODO: Include any routers here
    app.include_router(router)
    return app


app = create_app()
