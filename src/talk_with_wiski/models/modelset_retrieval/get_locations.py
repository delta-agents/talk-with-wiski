from pydantic import BaseModel, Field
from typing import Dict, List

from talk_with_wiski.models.base import ExampleBaseModel


class GetLocationsInput(ExampleBaseModel):
    """
    Input model for Example1Input tool.
    Currently, no parameters are required, but this can be extended in the future.
    """

    index: int = Field(
        ..., description="Index to use in the example tool. smaller than 5"
    )


class GetLocationsOutput(BaseModel):
    data: List[Dict[str, str]] = Field(..., description="data dictionary")
    description: str = Field(..., description="Table relationships")
