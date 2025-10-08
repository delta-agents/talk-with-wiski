from pydantic import BaseModel, Field
from typing import Dict, List

from talk_with_wiski.models.base import ExampleBaseModel


class GetParametersInput(ExampleBaseModel):
    """
    Input model for Example1Input tool.
    Currently, no parameters are required, but this can be extended in the future.
    """

    station_id: str|None = Field(
        None, description="Location for which to list all available parameters."
    )


class GetParametersOutput(BaseModel):
    data: List[Dict[str, str]] = Field(..., description="list of parameter dictionary")
    description: str = Field(..., description="Parameters")
