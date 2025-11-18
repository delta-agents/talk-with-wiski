"""
Example of a tool cal
"""

from talk_with_wiski.models.modelset_retrieval.get_timeseries_list import (
    GetTimeseriesListInput,
    GetTimeseriesListOutput,
)
from talk_with_wiski.utils.logging_utils import log_tool_call
import requests
import json


@log_tool_call
async def get_timeseries_list(
    ctx, input: GetTimeseriesListInput
) -> GetTimeseriesListOutput:
    """
    Show a list of available timeseries with metadata
    """

    #  you can access any context added to the ctx: Deps object
    url = ctx.deps.url

    # base url
    endpoint = url + "KiWIS"
    params = {
        "datasource": "0",
        "service": "kisters",
        "type": "queryServices",
        "request": "getTimeseriesList",
        "format": "objson",
        "returnfields": "station_name,station_no,station_id,ts_id,ts_name,parametertype_id,parametertype_name,ts_type_id,ts_type_name",
    }

    # extend url
    if input.station_no is not None:
        if isinstance(input.station_no, list):
            params["station_no"] = ",".join(input.station_no)
        else:
            params["station_no"] = input.station_no

    if input.site_no is not None:
        if isinstance(input.site_no, list):
            params["site_no"] = ",".join(input.site_no)
        else:
            params["site_no"] = input.site_no

    if input.parametertype_name is not None:
        if isinstance(input.parametertype_name, list):
            params["parametertype_name"] = ",".join(input.parametertype_name)
        else:
            params["parametertype_name"] = input.parametertype_name

    # request data
    res =  requests.get(endpoint, params=params, timeout=30)
    data = list(json.loads(res.text))

    return GetTimeseriesListOutput(
        data=data,
        description="list of available timeseries. The variable ts_id can be used as input for GetTimeseriesValuesInput",
    )
