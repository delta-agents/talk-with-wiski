"""
Timeseries: analyze availability of data
"""

from talk_with_wiski.models.modelset_retrieval.get_timeseries_values import (
    GetTimeseriesValuesOutput,
)
from talk_with_wiski.tools.toolset_retrieval.get_timeseries_values import (
    get_timeseries_values,
)
from talk_with_wiski.models.modelset_analysis.analyse_timeseries_availability import (
    AnalyseTimeseriesAvailabilityInput,
    AnalyseTimeseriesAvailabilityOutput,
)
from talk_with_wiski.utils.logging_utils import log_tool_call
import pandas as pd
from talk_with_wiski.utils import logger


@log_tool_call
async def analyse_timeseries_availability(
    ctx, input: AnalyseTimeseriesAvailabilityInput
) -> AnalyseTimeseriesAvailabilityOutput:
    """
    Determine availability of timeseries, input is a Timeseries class containing a single array of
    timeseries values.
    """
    dict_TimeseriesAvailability = {}
    output = await get_timeseries_values(ctx, input)
    df = _process_timeseries_values(output)
    #TODO: (optioneel) filteren op validatie-status?

    # availability analysis
    data_available = len(df) > 0
    dict_TimeseriesAvailability["available"] = data_available

    logger.debug("\n")
    logger.debug(f"data_available= {data_available}")

    # find period of availability data outside selected period
    if not data_available:
        # do a second get_timeseries_values call, with all values of input to None (except ts_id)
        input.from_date = None
        input.to_date = None
        input.period = "complete"
        input.futureperiod = None
        input.max_number_of_values_per_tsid = 1000000

        output = await get_timeseries_values(ctx, input)
        df = _process_timeseries_values(output)
        any_data_available = len(df) > 0
        if any_data_available:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df = df.sort_values(["timestamp"]).reset_index(drop=True)
            df = df.dropna()
            dict_TimeseriesAvailability["Tmin"] = df["timestamp"].min()
            dict_TimeseriesAvailability["Tmax"] = df["timestamp"].max()
        else:
            dict_TimeseriesAvailability["Tmin"] = pd.NaT
            dict_TimeseriesAvailability["Tmax"] = pd.NaT

    return AnalyseTimeseriesAvailabilityOutput(
        **dict_TimeseriesAvailability,
        description="availability of timeseries data",
    )


def _process_timeseries_values(output: GetTimeseriesValuesOutput) -> pd.DataFrame:
    data = output.model_dump()

    # make pandas dataframe to perform timeseries analysis
    records = []
    for timestamp, value in data["timeseries_values_list"][0][
        "data"
    ]:  # unpack the [timestamp, value] pairs
        records.append(
            {
                "timestamp": timestamp,
                "value": value,
            }
        )

    df = pd.DataFrame(records)
    return df
