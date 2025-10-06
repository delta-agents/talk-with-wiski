"""
Example of a tool call
"""

from talk_with_wiski.models.modelset_2.example2 import (
    Example2Input,
    Example2Output,
)
from talk_with_wiski.utils.logging_utils import log_tool_call


@log_tool_call
async def example2(ctx, input: Example2Input) -> Example2Output:
    """
    Show example2.
    """
    #  you can access any context added to the ctx: Deps object
    ctx.deps.cache_database_db
    data = {"example": 0, "of": 1, "how": 2, "data": 3, "might": 4, "look": 5}
    for val in data:
        data[val] = data[val] * input.factor
    return Example2Output(data=data, description="Example data")
