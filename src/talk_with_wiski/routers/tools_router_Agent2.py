from fastapi import APIRouter
from fastmcp import FastMCP
from talk_with_wiski.utils.docstring_generator import auto_docstring
from talk_with_wiski.models import (
    Example2Input,
    Example2Output,
)
from talk_with_wiski.tools import example2 as example1_pydanctic_ai

# Import tool functions and their models
from talk_with_wiski.routers.setup_connections import get_runtime_ctx

router = APIRouter()
mcp = FastMCP(name="Agent2")


# describe_timeseries tool registration
@mcp.tool()
@router.post("/tools.agent2/example2")
@auto_docstring("Example2")
async def example2(
    input: Example2Input,
) -> Example2Output:
    # TODO: add authentication passing to the get_runtime
    ctx = get_runtime_ctx()
    return await example1_pydanctic_ai(ctx, input)
