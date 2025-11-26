from pydantic import Field
from typing import List, Dict
import pandas as pd

from talk_with_wiski.models.modelset_retrieval.get_timeseries_values import (
    GetTimeseriesValuesInput,
    Timeseries,
)
from talk_with_wiski.models.base import WiskiBaseModel


class AnalyseTimeseriesQualityCodeInput(GetTimeseriesValuesInput):
    """
    Re-use Timeseries class from get_timeseries_values.
    """


class TimeseriesQualityCode(Timeseries):
    """Model representing a timeseries type."""
    
    
class AnalyseTimeseriesQualityCodeOutput(WiskiBaseModel):
    """Output is LinearTrendLine with slope and intercept for a given Timeseries class (containing timeseries_values
    for a certain ts_id)."""

    timeseries_quality_codes: List[Dict] = Field(
        ...,
        description="Quality codes for each timeseries.",
    )
    description: str = Field(
        ...,
        description="Quality codes for each timeseries.",
    )
