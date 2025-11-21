from pydantic import Field, model_validator
from pydantic_ai import ModelRetry
from typing import List, Optional

from talk_with_wiski.models.base import WiskiBaseModel


class GetTimeseriesTypeInput(WiskiBaseModel):
    """
    Input model for get_timeseries_type tool.
    """

    number_of_timeseries_types: int = Field(
        default=5, description="Number of timeseries types to retrieve"
    )
    ts_type_id: Optional[int] = Field(
        default=None,
        description="Timeseries type ID, retrieved from the tool `get_timeseries_list`",
    )
    ts_shortname: Optional[str | List[str]] = Field(
        default=None,
        description="Timeseries short name or names for which to list which type a timeseries is.",
    )
    ts_name: Optional[str | List[str]] = Field(
        default=None,
        description="Timeseries name or names for which to list which type a timeseries is.",
    )

    @model_validator(mode="after")
    def validate_exclusive_fields(self):
        ts_type_id, ts_shortname, ts_name = (
            self.ts_type_id,
            self.ts_shortname,
            self.ts_name,
        )
        if ts_shortname and ts_name:
            raise ModelRetry(
                "Only one of 'ts_shortname' or 'ts_name' can be provided, not both."
            )
        if len(set([ts_type_id, ts_shortname, ts_name])) == 1:
            raise ModelRetry(
                "One of the fields: 'ts_type_id, ts_shortname, ts_name' must be provided."
            )
        return self


class TimeseriesType(WiskiBaseModel):
    """Model representing a timeseries type."""

    ts_type_id: int
    ts_type_name: str
    ts_name: str
    ts_shortname: str


class GetTimeseriesTypeOutput(WiskiBaseModel):
    """Output model for GetTimeseriesTypeOutput tool."""

    timeseries_type_list: List[TimeseriesType] = Field(
        ..., description="list of Timeseries types"
    )
    description: str = Field(..., description="Timeseries type list description")
