from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TokenUsage(BaseModel):
    completion_tokens: int = Field(
        default=0, description="Number of completion_tokens used"
    )
    prompt_tokens: int = Field(default=0, description="Number of prompt_tokens used")
    total_tokens: int = Field(default=0, description="Total number of tokens used")
    completion_time: float = Field(
        default=0.0, description="Time taken for chat completion"
    )
    completion_tokens_details: Optional[dict] = Field(
        default_factory=dict, description="Details about completion tokens"
    )
    prompt_time: float = Field(default=0.0, description="Time taken for prompt")
    prompt_tokens_details: Optional[dict] = Field(
        default_factory=dict, description="Details about prompt tokens"
    )
    queue_time: float = Field(default=0.0, description="Time taken for queue")
    total_time: float = Field(default=0.0, description="Total time taken")

    model_config = ConfigDict(extra="ignore")


class ResponseMetadata(BaseModel):
    token_usage: TokenUsage = Field(
        default_factory=TokenUsage, description="Details about token usage"
    )
    model_name: str = Field(
        default="llama-3.1-8b-instant", description="Model used for response synthesis"
    )
    finish_reason: str = Field(
        default="stop", description="Reason that request finished"
    )
    model_provider: str = Field(
        default="groq", description="Model provider for request"
    )

    model_config = ConfigDict(extra="ignore")
