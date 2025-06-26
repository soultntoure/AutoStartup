from pydantic import BaseModel, Field
from typing import Literal

class IdeaClassification(BaseModel):
    """
    A model to hold the classification of a startup idea.
    """
    classification: Literal['software', 'strategic', 'vague'] = Field(
        ..., 
        description="The final classification of the idea."
    )
    reason: str = Field(
        ..., 
        description="A brief justification for why the idea was given this classification."
    )