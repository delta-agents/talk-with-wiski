from fastapi import APIRouter
from fastmcp import FastMCP
from talk_with_wiski.utils.docstring_generator import auto_docstring
from talk_with_wiski.models import (
    GetLocationsInput, 
    GetLocationsOutput,
    GetParametersInput,
    GetParametersOutput,
)
from talk_with_wiski.tools import get_locations as get_locations_pydanctic_ai
from talk_with_wiski.tools import get_parameters as get_parameters_pydantic_ai

# Import tool functions and their models
from talk_with_wiski.routers.setup_connections import get_runtime_ctx


router = APIRouter()
mcp = FastMCP(name="Wiski")

# describe_timeseries tool registration
@mcp.tool()
@router.post("/tools/get_locations")
@auto_docstring("get_locations")
async def get_locations(
    input: GetLocationsInput,
) -> GetLocationsOutput:
    # TODO: add authentication passing to the get_runtime
    ctx = get_runtime_ctx()
    return await get_locations_pydanctic_ai(ctx, input)

@mcp.tool()
@router.post("/tools/get_parameters")
@auto_docstring("get_parameters")
async def get_parameters(
    input: GetParametersInput,
) -> GetParametersOutput:
    # TODO: add authentication passing to the get_runtime
    ctx = get_runtime_ctx()
    return await get_parameters_pydantic_ai(ctx, input)
