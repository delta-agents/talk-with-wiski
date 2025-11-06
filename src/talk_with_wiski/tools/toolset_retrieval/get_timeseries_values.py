"""
Example of a tool cal
"""

from talk_with_wiski.models.modelset_retrieval.get_timeseries_values import (
    GetTimeseriesValuesInput,
    GetTimeseriesValuesOutput,
)
from talk_with_wiski.utils.logging_utils import log_tool_call
import requests
import json

@log_tool_call
async def get_timeseries_values(ctx, input: GetTimeseriesValuesInput) -> GetTimeseriesValuesOutput:
    """
    Show the timeseries data
    """

    #  you can access any context added to the ctx: Deps object
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

    # extend url
    if isinstance(input.ts_id, list):
        params["ts_id"] = ",".join(input.ts_id)
    else:
        params["ts_id"] = input.ts_id

    if input.from_date is not None:
        params["from"] = input.from_date

    if input.to_date is not None:
        params["to"] = input.to_date

    if input.period is not None:
        params["period"] = input.period

    if input.futureperiod is not None:
        params["futureperiod"] = input.futureperiod
    
    # requst data
    res = requests.get(endpoint, params=params)
    data = list(json.loads(res.text))

    return GetTimeseriesValuesOutput(data=data, description="Timeseries")
