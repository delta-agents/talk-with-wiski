"""
Example of a tool call
"""

from talk_with_wiski.models.modelset_retrieval.get_locations import (
    GetLocationsInput,
    GetLocationsOutput,
)
from talk_with_wiski.utils.logging_utils import log_tool_call

@log_tool_call
async def get_locations(ctx, input: GetLocationsInput) -> GetLocationsOutput:
    """
    get_locations from WISKI.
    contains only dummy data now
    """
    #  you can access any context added to the ctx: Deps object
    ctx.deps.cache_database_db
    data = { "loc1": {"name":"PAKT","x":2,"y":3},
             "loc2": {"name":"HAASNOOTD","x":-999,"y":999}}

    return GetLocationsOutput(data=data, description="Example data")
