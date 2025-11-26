"""
Timeseries: determine some statistics
"""

from talk_with_wiski.tools.toolset_retrieval.get_timeseries_values import (
    _get_timeseries_request,
)
from talk_with_wiski.models.modelset_analysis.analyse_timeseries_quality_code import (
    AnalyseTimeseriesQualityCodeInput,
    AnalyseTimeseriesQualityCodeOutput,
    TimeseriesQualityCode,
)
from talk_with_wiski.utils.logging_utils import log_tool_call

import pandas as pd
from collections import Counter

@log_tool_call
async def analyse_timeseries_quality_code(
    ctx, input: AnalyseTimeseriesQualityCodeInput
) -> AnalyseTimeseriesQualityCodeOutput:
    """
    Determine (statitics of) Quality Code of timeseries, by requesting an additonal returnfield from get_timeseries_values, 
    input is a (str) ts_id or a list of (str) timeseries ids.
    """
    input.max_number_of_values_per_tsid = 1000000
    input.max_number_of_tsids_to_retrieve = 100
    #input.returnfields='ts_id,Timestamp,Values,Quality%20Code%20Name'
    input.returnfields='Timestamp,Value,Quality Code Name'

    url = ctx.deps.url

    # base url
    endpoint = url + "KiWIS"
    params = {
        "datasource": "0",
        "service": "kisters",
        "type": "queryServices",
        "request": "getTimeseriesValues",
        "format": "dajson",
        "metadata": "true",
    }

    data = _get_timeseries_request(endpoint,input,params)
    
    n_ids = input.max_number_of_tsids_to_retrieve
    n_vals = input.max_number_of_values_per_tsid

    # data vullen
    timeseries_values_list = []
    for timeseries_values in data:
        timeseries_values["ts_id"] = int(timeseries_values["ts_id"])
        # limit number of data points
        timeseries_values["data"] = timeseries_values["data"][:n_vals]
        # Append as Timeseries object
        timeseries_values_list.append(TimeseriesQualityCode(**timeseries_values))

    #print(len(timeseries_values_list))
    #print(len(data[0]['data']))
    #print(data[0]['data'][:10])
    #print(data)

    # Get Quality Code Name counts into a dataframe
    results = []
    for ts in data:
        # ts['data'] is a list of lists: [Timestamp, Value, Quality Code Name]
        quality_codes = [row[2] for row in ts['data']]  # extract 3rd element
        counts = dict(Counter(quality_codes))           # count occurrences

        # you can store with other meta info
        result = {
            'ts_id': ts['ts_id'],
            'station_name': ts['station_name'],
            'station_no': ts['station_no'],
            'parametertype_name': ts['parametertype_name'],
            'n_datapoints': len(ts['data']),
            'quality_counts': counts
        }
        results.append(result)

    # Convert to DataFrame
    df_counts = pd.DataFrame(results)

    # Optional: expand quality_counts dict into separate columns
    df_counts_expanded = pd.concat(
        [df_counts.drop(columns='quality_counts'), df_counts['quality_counts'].apply(pd.Series)],
        axis=1
    )

    df_counts_expanded = df_counts_expanded.fillna(0)
    count_columns = df_counts_expanded.columns[5:]
    df_counts_expanded[count_columns] = df_counts_expanded[count_columns].astype(int)
    #print(df_counts_expanded)


    return AnalyseTimeseriesQualityCodeOutput(
        timeseries_quality_codes=df_counts_expanded.to_dict(orient="records"),
        description="List of Timeseries containing a Quality Code for each timeseries.",
    )
