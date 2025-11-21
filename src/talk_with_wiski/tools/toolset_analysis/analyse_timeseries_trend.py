"""
Linear trend analysis
"""

from talk_with_wiski.tools.toolset_retrieval.get_timeseries_values import get_timeseries_values
from talk_with_wiski.models.modelset_analysis.analyse_timeseries_trend import (
    AnalyseTimeseriesTrendInput,
    AnalyseTimeseriesTrendOutput,
    LinearTrendLine,
)
from talk_with_wiski.utils.logging_utils import log_tool_call


@log_tool_call
async def analyse_timeseries_trend(
    ctx, input: AnalyseTimeseriesTrendInput
) -> AnalyseTimeseriesTrendOutput:
    """
    Determine (linear) trend line of timeseries, input is a Timeseries class containing a single array of 
    timeseries values.
    """

    output = await get_timeseries_values(ctx, input)
    #print('\n')
    #print(type(output))

    data = output.model_dump()
    #print(type(data))
    #print(data)

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
    #print(df)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(["timestamp"]).reset_index(drop=True)
    df = df.dropna()

    # do some data-analysis on these time series
    #timeseries_analysis = timeseries_analyse(df, wlev_thresholds_dict)

    # Convert timestamp to numeric (seconds since start)
    df.loc[:, "time_numeric"] = (
        df["timestamp"] - df["timestamp"].min()
    ).dt.total_seconds()
    X = df["time_numeric"].values / 86400
    y = df["value"].values
    # : Fit linear regression
    n = len(X)

    # Calculate means
    mean_x = sum(X) / n
    mean_y = sum(y) / n

    # Calculate slope (a) and intercept (b)
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(X, y))
    denominator = sum((x - mean_x) ** 2 for x in X)

    slope = numerator / denominator
    intercept = mean_y - slope * mean_x

    #print(slope, intercept)

    linear_trend = LinearTrendLine(
        slope=slope,
        intercept=intercept,
    )

    return AnalyseTimeseriesTrendOutput(
        linear_trend_line=linear_trend,
        description="coefficients a (slope) and b (intercept) of linear trend line in provided data series",
    )
