from pydantic import UUID4, BaseModel, ConfigDict, Field, field_serializer


class ChatRequest(BaseModel):
    user_query: str = Field(..., description="The user's query for the chatbot.")
    user_id: UUID4 = Field(..., description="The unique identifier for the user.")
    session_id: UUID4 = Field(..., description="The unique identifier for the session.")

    @field_serializer("user_id", "session_id")
    def serialize_ids(self, value):
        return str(value)

    model_config = ConfigDict(extra="ignore")


class ChatResponse(BaseModel):
    user_query: str = Field(..., description="The user's query for the chatbot.")
