from typing import List, Optional

from pydantic import UUID4, BaseModel, ConfigDict, Field, field_serializer
from schemas.source import Source
from schemas.usage import ResponseMetadata


class ChatRequest(BaseModel):
    user_query: str = Field(..., description="The user's query for the chatbot.")
    user_id: UUID4 = Field(..., description="The unique identifier for the user.")
    session_id: UUID4 = Field(..., description="The unique identifier for the session.")

    @field_serializer("user_id", "session_id")
    def serialize_ids(self, value):
        return str(value)

    model_config = ConfigDict(extra="ignore")


class ChatResponse(BaseModel):
    # Business logic (Required Field)
    user_id: str = Field(..., description="Unique identifier for the user.")
    session_id: str = Field(..., description="Unique identifier for the session.")

    # User Query (Required Field)
    user_query: str = Field(..., description="User Query")

    # Sources
    sources: List[Source] = Field(
        default_factory=list, description="List of sources extracted from vector store"
    )

    # LLM Output
    content: Optional[str] = Field(default=None, description="LLM Response")

    # Metadata
    response_metadata: ResponseMetadata = Field(
        default_factory=ResponseMetadata, description="LLM Response Metadata"
    )

    model_config = ConfigDict(extra="ignore")
