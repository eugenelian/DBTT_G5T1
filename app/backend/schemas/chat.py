from datetime import datetime
from typing import List, Optional

from beanie import Document
from pydantic import (
    UUID4,
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
)
from schemas import now_utc
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


class ChatResponse(Document):
    # Business logic (Required Field)
    user_id: str = Field(..., description="Unique identifier for the user.")
    session_id: str = Field(..., description="Unique identifier for the session.")
    create_datetime: datetime = Field(
        default_factory=now_utc, description="UTC Datetime that document was created"
    )

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

    class Settings:
        name = "chat_responses"

    model_config = ConfigDict(extra="ignore")


class DiagnosisRequest(BaseModel):
    symptoms: list[str] = Field(
        default_factory=list, description="List of symptoms to generate diagnosis for"
    )
    remarks: Optional[str] = Field(default=None, description="Remarks from doctor")

    @field_validator("symptoms", mode="before")
    @classmethod
    def sanitize_symptoms(cls, v):
        if isinstance(v, list):
            return [
                item.replace("]]>", "] ]>") if isinstance(item, str) else item
                for item in v
            ]
        return v

    @field_validator("remarks", mode="before")
    @classmethod
    def sanitize_remarks(cls, v: Optional[str]) -> str:
        if not v:
            return "NIL"
        return v.replace("]]>", "] ]>")

    def get_user_prompt(self) -> str:
        return (
            f"Patient has the following symptoms: {self.symptoms}.\n"
            f"Doctor Remarks: {self.remarks}\n"
            "Share some possible diagnosis without any follow up questions."
        )

    model_config = ConfigDict(extra="ignore")
