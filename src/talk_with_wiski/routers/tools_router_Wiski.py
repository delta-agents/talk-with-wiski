from fastapi import APIRouter
from fastmcp import FastMCP
from talk_with_wiski.utils.docstring_generator import auto_docstring
from talk_with_wiski.models import (
    GetLocationsInput,
    GetLocationsOutput,
    GetParametersInput,
    GetParametersOutput,
    GetGroupListInput,
    GetGroupListOutput,
    GetSitesInput,
    GetSitesOutput,
)
from talk_with_wiski.tools import get_locations as get_locations_pydantic_ai
from talk_with_wiski.tools import get_parameters as get_parameters_pydantic_ai
from talk_with_wiski.tools import get_group_list as get_group_list_pydantic_ai
from talk_with_wiski.tools import get_sites as get_sites_pydantic_ai

# Import tool functions and their models
from talk_with_wiski.routers.setup_connections import get_runtime_ctx


router = APIRouter()
mcp = FastMCP(name="Wiski")


# describe_timeseries tool registration
@mcp.tool()
@router.post("/tools/get_locations")
@auto_docstring("Retrieves the locations from the WISKI API")
async def get_locations(
    input: GetLocationsInput,
) -> GetLocationsOutput:
    # TODO: add authentication passing to the get_runtime
    ctx = get_runtime_ctx()
    return await get_locations_pydantic_ai(ctx, input)


@mcp.tool()
@router.post("/tools/get_parameters")
@auto_docstring("Retrieves the parameters from the WISKI API")
async def get_parameters(
    input: GetParametersInput,
) -> GetParametersOutput:
    # TODO: add authentication passing to the get_runtime
    ctx = get_runtime_ctx()
    return await get_parameters_pydantic_ai(ctx, input)


@mcp.tool()
@router.post("/tools/get_sites")
@auto_docstring("Retrieves the sites information from the WISKI API")
async def get_sites(
    input: GetSitesInput,
) -> GetSitesOutput:
    ctx = get_runtime_ctx()
    return await get_sites_pydantic_ai(ctx, input)


@mcp.tool()
@router.post("/tools/get_group_list")
@auto_docstring("Retrieves the group list from the WISKI API")
async def get_group_list(
    input: GetGroupListInput,
) -> GetGroupListOutput:
    # TODO: add authentication passing to the get_runtime
    ctx = get_runtime_ctx()
    return await get_group_list_pydantic_ai(ctx, input)
