from pydantic import Field
from typing import Dict

from talk_with_wiski.models.base import WiskiBaseModel


class AddIndexInput(WiskiBaseModel):
    """
    Input model for AddIndex tool.
    Requires index as an input.
    """

    index: int = Field(
        ..., description="Index to use in the add_index tool. smaller than 5"
    )
    index2: int = Field(
        2, description="optional Second index to use in the add_index tool, default 2"
    )


class AddIndexOutput(WiskiBaseModel):
    data: Dict[str, int] = Field(..., description="data dictionary")
    description: str = Field(..., description="Table relationships")
