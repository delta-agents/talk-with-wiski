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

@log_tool_call
async def get_parameters(ctx, station_id: GetParametersInput) -> GetParametersOutput:
    """
    Show available parameters for a measurement station
    """

    #  you can access any context added to the ctx: Deps object
    url = ctx.deps.url
    # endpoint = url + 'KiWIS?datasource=0&service=kisters&type=queryServices&request=getParameterList&format=objson'
    endpoint = url + 'KiWIS'
    params={'datasource': '0',
            'service': 'kisters',
            'type': 'queryServices',
            'request': 'getParameterList',
            'format': 'objson',
            }
    if station_id.station_id is not None:
        params['station_id'] = station_id.station_id

    res = requests.get(endpoint, params=params)
    data = list(json.loads(res.text))
    
    # location = location.index
    # data = [
    #     {"parameter": "hoogte", "eenheid": "m"},
    #     {"parameter": "regenval", "eenheid": "mm"},
    #     {"parameter": "debiet", "eenheid": "m3/s"},
    # ]
    # if location == "Loc1":
    #     data.append({"parameter": "stroomsnelheid", "eenheid": "m/s"})

    return GetParametersOutput(data=data, description="Parameters")
