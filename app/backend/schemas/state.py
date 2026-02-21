from pydantic import BaseModel, ConfigDict, Field

class State(BaseModel):
    """A base state object for a RAG Workflow."""

    # Business logic
    user_id: str = Field(..., description="Unique identifier for the user.")
    session_id: str = Field(..., description="Unique identifier for the session.")

    # User Query
    user_query: str = Field(..., description="User Query")

    # LLM Output
    content: str = Field(default=None, description="LLM Response")

    # Usage Data
    usage: dict = Field(default={}, description="LLM Usage Data")

    model_config = ConfigDict(
        extra="ignore"
    )
