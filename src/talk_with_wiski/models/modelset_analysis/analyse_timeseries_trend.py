from pydantic import BaseModel, Field

from talk_with_wiski.models.modelset_retrieval.get_timeseries_values import GetTimeseriesValuesInput
from talk_with_wiski.models.base import ExampleBaseModel



class AnalyseTimeseriesTrendInput(GetTimeseriesValuesInput):
    """
    Re-use Timeseries class from get_timeseries_values.
    """
    # Inherits from Timeseries, add or overwrite features below.
    ts_id: str = Field(
            default=None,
            description="SINGLE ts_id as string for timeseries analysis",
        )


class LinearTrendLine(BaseModel):
    """Model representing a trend line for a timeseries."""

    slope: float
    intercept: float


class AnalyseTimeseriesTrendOutput(ExampleBaseModel):
    """Output is LinearTrendLine with slope and intercept for a given Timeseries class (containing timeseries_values
       for a certain ts_id)."""

    linear_trend_line: LinearTrendLine = Field(
        ..., description="Linear trend line with slope (cm/day) and intercept."
    )
    description: str = Field(..., description="Linear trend line with slope and intercept.")
