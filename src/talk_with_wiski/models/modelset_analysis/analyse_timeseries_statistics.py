from pydantic import BaseModel, Field

from talk_with_wiski.models.modelset_retrieval.get_timeseries_values import GetTimeseriesValuesInput
from talk_with_wiski.models.base import ExampleBaseModel



class AnalyseTimeseriesStatsInput(GetTimeseriesValuesInput):
    """
    Re-use Timeseries class from get_timeseries_values.
    """
    # Inherits from Timeseries, add or overwrite features below.
    ts_id: str = Field(
            default=None,
            description="SINGLE ts_id as string for timeseries analysis",
        )


class TimeseriesStatistics(BaseModel):
    """Model representing a trend line for a timeseries."""

    minimum: float
    maximum: float
    average: float
    stddev: float


class AnalyseTimeseriesStatsOutput(ExampleBaseModel):
    """Output is LinearTrendLine with slope and intercept for a given Timeseries class (containing timeseries_values
       for a certain ts_id)."""

    timeseries_statistics: TimeseriesStatistics = Field(
        ..., description="Statistics of a given timeseries such as min/max/average/stddev."
    )
    description: str = Field(..., description="Statistics of a given timeseries such as min/max/average/stddev.")
