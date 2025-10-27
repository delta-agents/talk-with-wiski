"""
Example of a tool cal
"""

from talk_with_wiski.models.modelset_retrieval.get_parameters import (
    GetParametersInput,
    GetParametersOutput,
)
from talk_with_wiski.utils.logging_utils import log_tool_call
import requests
import json
from itertools import compress


@log_tool_call
async def get_parameters(ctx, input: GetParametersInput) -> GetParametersOutput:
    """
    Show available parameters for a measurement station
    """

    #  you can access any context added to the ctx: Deps object
    url = ctx.deps.url

    # base url
    endpoint = url + "KiWIS"
    params = {
        "datasource": "0",
        "service": "kisters",
        "type": "queryServices",
        "request": "getParameterList",
        "format": "objson",
        "returnfields": "station_name,station_no,station_id,parametertype_id,parametertype_name,stationparameter_name,stationparameter_longname",
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

    # if input.parametertype_name is not None:
    #     if isinstance(input.parametertype_name, list):
    #         params['parametertype_name'] = ','.join(input.parametertype_name)
    #     else:
    #         params['parametertype_name'] = input.parametertype_name

    # requst data
    res = requests.get(endpoint, params=params)
    data = list(json.loads(res.text))

    # filter results
    if input.parameter_type is not None:
        idx = [
            input.parameter_type.lower() in row["stationparameter_name"].lower()
            for row in data
        ]
        data = list(compress(data, idx))

    # location = location.index
    # data = [
    #     {"parameter": "hoogte", "eenheid": "m"},
    #     {"parameter": "regenval", "eenheid": "mm"},
    #     {"parameter": "debiet", "eenheid": "m3/s"},
    # ]
    # if location == "Loc1":
    #     data.append({"parameter": "stroomsnelheid", "eenheid": "m/s"})

    return GetParametersOutput(data=data, description="Parameters")
