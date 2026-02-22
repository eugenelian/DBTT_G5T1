from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class SourceMetadata(BaseModel):
    source: str = Field(default="", description="Source URL/filename of the resource")
    title: str = Field(default="", description="Title of resource")
    description: str = Field(default="", description="Description of the resource")
    language: str = Field(default="en", description="Language used in the resource")

    model_config = ConfigDict(extra="ignore")


class Source(BaseModel):
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique identifier of the Source",
    )
    metadata: SourceMetadata = Field(default_factory=SourceMetadata)
    page_content: str = Field(default="", description="Page Contents of source")
    type: str = Field(default="Document", description="Type of Source")

    model_config = ConfigDict(extra="ignore")
