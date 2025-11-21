from pydantic import Field

from talk_with_wiski.models.modelset_retrieval.get_timeseries_values import (
    GetTimeseriesValuesInput,
)
from talk_with_wiski.models.base import WiskiBaseModel


class AnalyseTimeseriesThresholdsInput(GetTimeseriesValuesInput):
    """
    Re-use Timeseries class from get_timeseries_values.
    """

    # Inherits from Timeseries, add or overwrite features below.
    ts_id: str = Field(
        default=None,
        description="SINGLE ts_id as string for timeseries analysis",
    )
    threshold: float = Field(
        default=None,
        description="Threshold value for timeseries analysis",
    )


class TimeseriesThresholds(WiskiBaseModel):
    """Model representing a trend line for a timeseries."""

    threshold_value: float
    total_time_above_in_hours: float


class AnalyseTimeseriesThresholdsOutput(WiskiBaseModel):
    """Output is LinearTrendLine with slope and intercept for a given Timeseries class (containing timeseries_values
    for a certain ts_id)."""

    threshold_values: TimeseriesThresholds = Field(
        ...,
        description="Threshold analysis on timeseries using pre-defined thresholds.",
    )
    description: str = Field(
        ...,
        description="Threshold analysis on timeseries using pre-defined thresholds.",
    )
