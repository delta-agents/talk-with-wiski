from pydantic import Field, model_validator
from pydantic_ai import ModelRetry
from typing import List, Optional

from talk_with_wiski.models.base import WiskiBaseModel


class GetTimeseriesValuesInput(WiskiBaseModel):
    """
    Input model for GetTimeseriesValuesInput tool.
    """

    ts_id: str | List[str] = Field(
        default=None,
        description="Timeseries ID or IDs for which to provide all timeseries data. This variable can be obtained from getTimeseriesListOutput (the output of the function get_timeseries_list)",
    )
    max_number_of_tsids_to_retrieve: int = Field(
        # max_number_of_tsids_to_retrieve of LIMIT? increase if you want....
        default=5,
        description="Maximum number of timeseries_id to retrieve, default=5, increase this parameter"
        "if you need data for more timeseries_ids",
    )
    max_number_of_values_per_tsid: int = Field(
        # max_number_of_values_per_tsid
        default=10,
        description="Maximum number of values per timeseries_id to retrieve, default=10, increase this parameter"
        "if you need data for more values per timeseries_ids",
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
    returnfields: Optional[str] = Field(
        default=None,
        description="Comma-separated list of fields (spaces allowed) to include in the response. If not specified, all default fields will be included.",
    )
    get_as_url: Optional[bool] = Field(
        default=False,
        description="Option to get url instead of data in case of large data requests",
    )
    include_quality_codes: Optional[bool] = Field(
        default=False,
        description="Option to include quality codes in the response",
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


class Timeseries(WiskiBaseModel):
    """Model representing a timeseries type."""

    ts_id: int
    station_name: str
    station_no: str
    data: List


class GetTimeseriesValuesOutput(WiskiBaseModel):
    """Output model for GetTimeseriesValuesOutput tool."""

    timeseries_values_list: List[Timeseries] = Field(
        ...,
        description="List of Timeseries objects with values; if include_quality_codes is True, data includes quality code keys (which can be matched with quality code table)",
    )
    description: str = Field(..., description="Timeseries values")
    url: str = Field(
        ..., description="URL that is returned upon request by using get_as_url"
    )
