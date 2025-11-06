from pydantic import BaseModel, Field, model_validator
from pydantic_ai import ModelRetry
from typing import Dict, List, Optional

from talk_with_wiski.models.base import ExampleBaseModel


class GetTimeseriesValuesInput(ExampleBaseModel):
    """
    Input model for Example1Input tool.
    Currently, no parameters are required, but this can be extended in the future.
    """

    ts_id: str | List[str] = Field(
        default=None,
        description="Timeseries ID or IDs for which to provide all timeseries data. This variable can be obtained from getTimeseriesListOutput (the output of the function get_timeseries_list)",
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

    @model_validator(mode="after")
    def validate_exclusive_fields(cls, values):
        ts_id, from_date, to_date, period, futureperiod = (
            values.ts_id,
            values.from_date,
            values.to_date,
            values.period,
            values.futureperiod,
        )
        if not ts_id:
            raise ModelRetry(
                "'ts_id' must be provided."
            )
        elif not (from_date or to_date or period or futureperiod):
            raise ModelRetry(
                "At least one of the arguments 'from', 'to', 'period' or 'futureperiod' must be provided."
            )
        elif (from_date and to_date) and not (period or futureperiod):
            return values
        elif (from_date and period) and not (to_date or futureperiod):
            return values
        elif (to_date and period) and not (from_date or futureperiod):
            return values
        elif (period) and not (from_date or to_date or futureperiod):
            return values
        elif (from_date) and not (to_date or period or futureperiod):
            return values
        elif (to_date) and not (from_date or period or futureperiod):
            return values
        elif (futureperiod) and not (from_date or to_date or period):
            return values
        elif (period and futureperiod) and not (from_date or to_date):
            return values
        elif (from_date and futureperiod) and not (to_date or period):
            return values
        else:
            raise ModelRetry(
                "This combination of 'from', 'to', 'period' and 'futureperiod' is not valid. Please provide one of these combinations: 'from' and 'to', 'from' and 'period', 'to' and 'period', 'period', 'from', 'to', 'futureperiod', 'period' and 'futureperiod', or 'from' and 'futureperiod'."
            )


class GetTimeseriesValuesOutput(BaseModel):
    data: List[Dict[str, str | List]] = Field(..., description="timeseries data")
    description: str = Field(..., description="Timeseries data")