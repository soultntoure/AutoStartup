# src/autostartup/models.py
from pydantic import BaseModel, Field
from typing import Literal

class IdeaClassification(BaseModel):
    classification: Literal["software", "strategic", "vague"] = Field(
        description="The category of the startup idea"
    )
    confidence: float = Field(
        ge=0.0, 
        le=1.0, 
        description="Confidence score between 0 and 1"
    )
    reasoning: str = Field(
        description="Brief explanation for the classification"
    )