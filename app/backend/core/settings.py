import logging
import re
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

_PATTERN = re.compile(
    r"ID|ENDPOINT|SECRET|ALGORITHM|CONNECTION_STRING|HOST|PORT|ACCESS_KEY|KEY",
    re.IGNORECASE,
)


class Settings(BaseSettings):
    # Replace these with your own values, either in environment variables or directly here

    # LLM Client
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4.1-mini"
    GROQ_API_KEY: str | None = None
    GROQ_MODEL: str = "llama-3.1-8b-instant"

    # LangChain/LangSmith Configuration
    LANGCHAIN_API_KEY: str | None = None
    LANGCHAIN_TRACING_V2: str | None = "false"
    LANGCHAIN_PROJECT: str | None = None

    def get_shareable_config(self) -> dict:
        config = super().model_dump()
        return {k: v for k, v in config.items() if not _PATTERN.search(k)}

    model_config = SettingsConfigDict(env_file_encoding="utf-8", extra="ignore")


@lru_cache  # builds once, the first time it’s asked for
def get_settings() -> Settings:
    return Settings()
