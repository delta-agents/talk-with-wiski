"""
Example of a tool cal
"""

from talk_with_wiski.models.modelset_retrieval.get_timeseries_type import (
    GetTimeseriesTypeInput,
    GetTimeseriesTypeOutput,
    TimeseriesType,
)
from talk_with_wiski.utils.logging_utils import log_tool_call
import requests
import json


@log_tool_call
async def get_timeseries_type(
    ctx, input: GetTimeseriesTypeInput
) -> GetTimeseriesTypeOutput:
    """
    Show available timeseries types
    """

    #  you can access any context added to the ctx: Deps object
    url = ctx.deps.url

    # base url
    endpoint = url + "KiWIS"
    params = {
        "datasource": "0",
        "service": "kisters",
        "type": "queryServices",
        "request": "getTimeseriesTypeList",
        "format": "objson",
        "returnfields": "ts_type_id,ts_type_name,ts_name,ts_shortname",
    }

    # extend url
    if input.ts_shortname is not None:
        if isinstance(input.ts_shortname, list):
            params["ts_shortname"] = ",".join(input.ts_shortname)
        else:
            params["ts_shortname"] = input.ts_shortname

    if input.ts_name is not None:
        if isinstance(input.ts_name, list):
            params["ts_name"] = ",".join(input.ts_name)
        else:
            params["ts_name"] = input.ts_name

    if input.ts_type_id is not None:
        if isinstance(input.ts_type_id, list):
            params["ts_type_id"] = ",".join(input.ts_type_id)
        else:
            params["ts_type_id"] = input.ts_type_id

    # requst data
    res =  requests.get(endpoint, params=params, timeout=30)
    data = list(json.loads(res.text))

    timeseries_type_list = []
    for timeseries_type in data:
        timeseries_type["ts_type_id"] = int(timeseries_type["ts_type_id"])
        timeseries_type_list.append(TimeseriesType(**timeseries_type))

    n = input.number_of_timeseries_types
    timeseries_type_list = timeseries_type_list[:n]
    description = f"Timeseries type list retrieved successfully, containing a total of  {len(timeseries_type_list)} items."
    if len(timeseries_type_list) > n:
        description += f"Only the first {n} items are returned, search for specific items using the provided filters or increase the number of items requested."
    return GetTimeseriesTypeOutput(
        timeseries_type_list=timeseries_type_list, description=description
    )
