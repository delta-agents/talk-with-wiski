"""
Example of a tool cal
"""

from talk_with_wiski.models.modelset_retrieval.get_parameters import (
    GetParametersInput,
    GetParametersOutput,
)
from talk_with_wiski.utils.logging_utils import log_tool_call
import requests

@log_tool_call
async def get_parameters(ctx, location: GetParametersInput) -> GetParametersOutput:
    """
    Show available parameters for a measurement station
    """
    #  you can access any context added to the ctx: Deps object
    url = ctx.deps.url
    endpoint = url + 'KiWIS?datasource=0&service=kisters&type=queryServices&request=getParameterList&format=objson'
    res = requests.get(endpoint)
    data = dict(res.json())

    # location = location.index
    # data = [
    #     {"parameter": "hoogte", "eenheid": "m"},
    #     {"parameter": "regenval", "eenheid": "mm"},
    #     {"parameter": "debiet", "eenheid": "m3/s"},
    # ]
    # if location == "Loc1":
    #     data.append({"parameter": "stroomsnelheid", "eenheid": "m/s"})

    return GetParametersOutput(data=data, description="Parameters")
