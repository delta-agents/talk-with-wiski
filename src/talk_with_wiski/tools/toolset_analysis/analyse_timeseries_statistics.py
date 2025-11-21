"""
Timeseries: determine some statistics
"""

from talk_with_wiski.tools.toolset_retrieval.get_timeseries_values import get_timeseries_values
from talk_with_wiski.models.modelset_analysis.analyse_timeseries_statistics import (
    AnalyseTimeseriesStatsInput,
    AnalyseTimeseriesStatsOutput,
    TimeseriesStatistics,
)
from talk_with_wiski.utils.logging_utils import log_tool_call
import numpy as np

@log_tool_call
async def analyse_timeseries_statistics(
    ctx, input: AnalyseTimeseriesStatsInput
) -> AnalyseTimeseriesStatsOutput:
    """
    Determine statistics of timeseries such as min/max/avg/stddev, input is a Timeseries class containing a single array of 
    timeseries values.
    """

    output = await get_timeseries_values(ctx, input)
    data = output.model_dump()

    # make pandas dataframe to perform timeseries analysis
    import pandas as pd
    records = []
    for timestamp, value in data["timeseries_values_list"][0]["data"]:  # unpack the [timestamp, value] pairs
        records.append(
            {
                "timestamp": timestamp,
                "value": value,
            }
        )

    df = pd.DataFrame(records)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(["timestamp"]).reset_index(drop=True)
    df = df.dropna()

    timeseries_statistics = TimeseriesStatistics(
        minimum = np.nanmin(df["value"]),
        maximum = np.nanmax(df["value"]),
        average = np.nanmean(df["value"]),
        stddev = np.nanstd(df["value"]),
    )

    return AnalyseTimeseriesStatsOutput(
        timeseries_statistics=timeseries_statistics,
        description="Statistics of timeseries",
    )
