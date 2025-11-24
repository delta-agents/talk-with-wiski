from typing import Optional, Tuple, Any
from pydantic import Field

from talk_with_wiski.models.modelset_retrieval.get_timeseries_values import (
    GetTimeseriesValuesInput,
)
from talk_with_wiski.models.base import WiskiBaseModel


class AnalyseTimeseriesAvailabilityInput(GetTimeseriesValuesInput):
    """
    Re-use Timeseries class from get_timeseries_values.
    """

    # Inherits from Timeseries, add or overwrite features below.
    ts_id: str = Field(
        default=None,
        description="SINGLE ts_id as string for timeseries analysis",
    )


class AnalyseTimeseriesAvailabilityOutput(WiskiBaseModel):
    """Output is data availability for a given Timeseries class (containing timeseries_values
    for a certain ts_id)."""

    available: bool = Field(
        ...,
        description="Availability of any timeseries data for the given ts_id and time period",
    )
    Tmin: Optional[Any] = Field(
        default=None,
        description="First timestamp with available data for the given ts_id. This argument is only provided if data is not available within the selected period.",
    )
    Tmax: Optional[Any] = Field(
        default=None,
        description="Last timestamp with available data for the given ts_id. This argument is only provided if data is not available within the selected period.",
    )
    description: str = Field(
        ...,
        description="Availability analysis on timeseries using pre-defined thresholds.",
    )
