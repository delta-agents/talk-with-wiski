from pydantic import BaseModel, Field, model_validator
from pydantic_ai import ModelRetry
from typing import List, Optional

from talk_with_wiski.models.base import ExampleBaseModel


class GetTimeseriesValuesInput(ExampleBaseModel):
    """
    Input model for GetTimeseriesValuesInput tool.
    """

    ts_id: str | List[str] = Field(
        default=None,
        description="Timeseries ID or IDs for which to provide all timeseries data. This variable can be obtained from getTimeseriesListOutput (the output of the function get_timeseries_list)",
    )
    number_of_tsids_to_retrieve: int = Field(
        default=5, description="Number of timeseries_id to retrieve"
    )
    number_of_values_per_tsid: int = Field(
        default=10, description="Number of timeseries values per id to retrieve"
    )
    from_date: Optional[str] = Field(
        default=None,
        description="Start date for the timeseries data request. Format must be yyyy-MM-dd or yyyy-MM-dd'T'HH:mm:ss'Z'",
    )
    to_date: Optional[str] = Field(
        default=None,
        description="End date for the timeseries data request. Format must be yyyy-MM-dd or yyyy-MM-dd'T'HH:mm:ss'Z'",
    )
    period: Optional[str] = Field(
        default=None,
        description="Time period for historical timeseries data request. Must be according to ISO format P#Y#M#DT#H#M#S where P just indicates an arbitrary period with the # being integers. 'period=complete' will return the complete coverage of all requested timeseries",
    )
    futureperiod: Optional[str] = Field(
        default=None,
        description="Future time period for future timeseries data request. Must be according to ISO format P#Y#M#DT#H#M#S where P just indicates an arbitrary period with the # being integers",
    )
    get_as_url: Optional[bool] = Field(
        default=False,
        description="Option to get url instead of data in case of large data requests",
    )

    @model_validator(mode="after")
    def validate_exclusive_fields(self):
        ts_id, from_date, to_date, period, futureperiod = (
            self.ts_id,
            self.from_date,
            self.to_date,
            self.period,
            self.futureperiod,
        )
        if not ts_id:
            raise ModelRetry("'ts_id' must be provided.")
        elif not (from_date or to_date or period or futureperiod):
            raise ModelRetry(
                "At least one of the arguments 'from', 'to', 'period' or 'futureperiod' must be provided."
            )
        elif (from_date and to_date) and not (period or futureperiod):
            return self
        elif (from_date and period) and not (to_date or futureperiod):
            return self
        elif (to_date and period) and not (from_date or futureperiod):
            return self
        elif (period) and not (from_date or to_date or futureperiod):
            return self
        elif (from_date) and not (to_date or period or futureperiod):
            return self
        elif (to_date) and not (from_date or period or futureperiod):
            return self
        elif (futureperiod) and not (from_date or to_date or period):
            return self
        elif (period and futureperiod) and not (from_date or to_date):
            return self
        elif (from_date and futureperiod) and not (to_date or period):
            return self
        else:
            raise ModelRetry(
                "This combination of 'from', 'to', 'period' and 'futureperiod' is not valid. Please provide one of these combinations: 'from' and 'to', 'from' and 'period', 'to' and 'period', 'period', 'from', 'to', 'futureperiod', 'period' and 'futureperiod', or 'from' and 'futureperiod'."
            )


class Timeseries(BaseModel):
    """Model representing a timeseries type."""

    ts_id: int
    station_name: str
    data: List


class GetTimeseriesValuesOutput(BaseModel):
    """Output model for GetTimeseriesValuesOutput tool."""

    timeseries_values_list: List[Timeseries] = Field(
        ..., description="List of Timeseries objects with values"
    )
    description: str = Field(..., description="Timeseries values")
    url: str = Field(
        ..., description="URL that is returned upon request by using get_as_url"
    )
