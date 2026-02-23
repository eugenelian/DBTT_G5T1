from pydantic import BaseModel, ConfigDict, Field


class State(BaseModel):
    """A base state object for a RAG Workflow."""

    # Business logic  (Required Field)
    user_id: str = Field(..., description="Unique identifier for the user.")
    session_id: str = Field(..., description="Unique identifier for the session.")

    # User Query (Required Field)
    user_query: str = Field(..., description="User Query")

    # Conversation History
    conversation_history: list[dict] = Field(
        default_factory=list,
        description="List of conversation history within the same session",
    )

    # Sources
    sources: list[dict] = Field(
        default_factory=list, description="List of sources extracted from vector store"
    )

    # LLM Output
    content: str | None = Field(default=None, description="LLM Response")

    # Usage Data
    response_metadata: dict = Field(
        default_factory=dict, description="LLM Response Metadata"
    )

    model_config = ConfigDict(extra="ignore")
