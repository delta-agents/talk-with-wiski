"""
Timeseries: analyze exceedance of thresholds
"""

from talk_with_wiski.tools.toolset_retrieval.get_timeseries_values import get_timeseries_values
from talk_with_wiski.models.modelset_analysis.analyse_timeseries_thresholds import (
    AnalyseTimeseriesThresholdsInput,
    AnalyseTimeseriesThresholdsOutput,
    TimeseriesThresholds,
)
from talk_with_wiski.utils.logging_utils import log_tool_call


@log_tool_call
async def analyse_timeseries_thresholds(
    ctx, input: AnalyseTimeseriesThresholdsInput
) -> AnalyseTimeseriesThresholdsOutput:
    """
    Determine thresholds of timeseries, input is a Timeseries class containing a single array of 
    timeseries values.
    """

    threshold = input.threshold
    
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

    # tijdsduur boven een grenswaarde
    # Step 1: mark above threshold
    df.loc[:, "above"] = df["value"] > threshold
    # Step 2: compute time differences between consecutive timestamps
    df.loc[:, "dt"] = df["timestamp"].diff().shift(-1)  # time to next row
    # Step 3: sum durations only for rows where value is above threshold
    total_time_above = df.loc[df["above"], "dt"].sum()
    total_time_above_in_hours = total_time_above / pd.Timedelta(hours=1)

    #print('\n')        
    #print(threshold)        
    #print(total_time_above_in_hours)        

    threshold_values = TimeseriesThresholds(
        threshold_value=threshold,
        total_time_above_in_hours=total_time_above_in_hours,
    )

    return AnalyseTimeseriesThresholdsOutput(
        threshold_values=threshold_values,
        description="exceedance time in hours of thresholds in provided data series",
    )
