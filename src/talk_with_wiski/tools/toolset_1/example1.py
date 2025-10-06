from talk_with_wiski.models.modelset_1.example1 import (
    AddIndexInput,
    AddIndexOutput,
)
from talk_with_wiski.utils.logging_utils import log_tool_call


@log_tool_call
async def add_index(ctx, input: AddIndexInput) -> AddIndexOutput:
    """
    adds the index to the data provided
    """
    #  you can access any context added to the ctx: Deps object
    ctx.deps.cache_database_db
    data = {"example": 0, "of": 1, "how": 2, "data": 3, "might": 4, "look": 5}
    new_data = {}
    for val in data:
        new_data[val] = data[val] + input.index
    return AddIndexOutput(data=new_data, description="Example data")
