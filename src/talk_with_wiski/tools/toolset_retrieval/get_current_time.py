"""
Tool to get the current time
"""

import datetime
from talk_with_wiski.models.modelset_retrieval.get_current_time import (
    GetCurrentTimeInput,
    GetCurrentTimeOutput,
)
from talk_with_wiski.utils.logging_utils import log_tool_call
from talk_with_wiski.utils.logging_utils import logger


@log_tool_call
async def get_current_time(ctx, input: GetCurrentTimeInput) -> GetCurrentTimeOutput:
    """
    Return the current time
    """
    #  you can access any context added to the ctx: Deps object
    current_time = datetime.datetime.now().isoformat()

    logger.debug("Current time:", len(current_time))

    return GetCurrentTimeOutput(
        current_time=current_time, description="Current time as ISO formatted string"
    )
