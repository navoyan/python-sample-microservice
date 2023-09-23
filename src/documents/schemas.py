from enum import Enum
from pydantic import BaseModel, Field


class DocumentStatus(str, Enum):
    INITIATED = "INITIATED"
    IN_REVIEW = "IN_REVIEW"
    APPROVED = "APPROVED"


class BaseDocument(BaseModel):
    body: str = Field(examples=["Some cool content"])
    status: DocumentStatus = Field(examples=["INITIATED"])
    comments: list[str] = Field(examples=[["Very good!", "Awesome!"]])


class DocumentCreateRequest(BaseDocument):
    pass


class DocumentUpdateRequest(BaseModel):
    body: str | None = None
    status: DocumentStatus | None = None
    comments: list[str] | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "body": "Only changed content"
                }
            ]
        }
    }


class DocumentResponse(BaseDocument):
    id: str = Field(examples=["650e113b690378865e46769e"])
