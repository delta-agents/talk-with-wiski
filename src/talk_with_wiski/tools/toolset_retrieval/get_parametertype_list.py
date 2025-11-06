"""
Example of a tool cal
"""

from talk_with_wiski.models.modelset_retrieval.get_parametertype_list import (
    GetParametertypeListInput,
    GetParametertypeListOutput,
)
from talk_with_wiski.utils.logging_utils import log_tool_call
from talk_with_wiski.utils.logging_utils import logger

import requests
import json


@log_tool_call
async def get_parametertype_list(
    ctx, input: GetParametertypeListInput
) -> GetParametertypeListOutput:
    """
    Show list of available parametertypes, either get id or list of parameters using a wildcard
    """

    #  you can access any context added to the ctx: Deps object
    ctx.deps.cache_database_db
    url = ctx.deps.url

    # base url
    endpoint = (
        url
        + "KiWIS?datasource=0&service=kisters&type=queryServices&request=getParameterTypeList&format=objson"
    )

    # extend url
    if getattr(input, "parametertype_id", None):
        endpoint += "&parametertype_id=" + ",".join(map(str, input.parametertype_id))

    if getattr(input, "parametertype_name", None):
        endpoint += "&parametertype_name=" + ",".join(
            map(str, input.parametertype_name)
        )

    # For debugging
    logger.debug(endpoint)
    logger.debug("\n".join(endpoint.split("&")))

    # call to KiWIS API
    res = requests.get(endpoint)
    # maak er een json object van om terug te geven (default)
    data = json.loads(res.text)

    # for d in data:
    #    d['parametertype_id'] = int(d['parametertype_id'])
    logger.debug(data)

    return GetParametertypeListOutput(
        data=data, description="ParametertypeList obtained from KiWIS API"
    )
