from pydantic import Field
from typing import Dict

from talk_with_wiski.models.base import WiskiBaseModel


class GetQualityCodeTableInput(WiskiBaseModel):
    """
    Input model for get_timeseries_metadata tool.
    ts_id is required (string or list of strings).
    """

    # no input required


class GetQualityCodeTableOutput(WiskiBaseModel):
    data: Dict = Field(
        ...,
        description="Table (dict) containing translation between Quality Code (Key, int), its name and description.",
    )
    description: str = Field(
        ...,
        description="Table (dict) containing translation between Quality Code (Key, int), its name and description.",
    )
