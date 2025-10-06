from pydantic import BaseModel, Field
from typing import Dict

from talk_with_wiski.models.base import ExampleBaseModel


class Example2Input(ExampleBaseModel):
    """
    Input model for Example2Input tool.
    Currently, no parameters are required, but this can be extended in the future.
    """

    factor: int = Field(..., description="A factor for the example2 tool")


class Example2Output(BaseModel):
    data: Dict[str, int] = Field(..., description="data dictionary")
    description: str = Field(..., description="Description of the example2 output")
