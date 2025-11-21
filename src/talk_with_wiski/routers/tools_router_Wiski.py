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
    GetParametertypeListInput,
    GetParametertypeListOutput,
    GetTimeseriesListInput,
    GetTimeseriesListOutput,
    GetTimeseriesValuesInput,
    GetTimeseriesValuesOutput,
    GetTimeseriesTypeInput,
    GetTimeseriesTypeOutput,
    # TimeseriesType,
    AnalyseTimeseriesTrendInput,
    AnalyseTimeseriesTrendOutput,
    # LinearTrendLine,
    AnalyseTimeseriesStatsInput,
    AnalyseTimeseriesStatsOutput,
    # TimeseriesStatistics,
    AnalyseTimeseriesThresholdsInput,
    AnalyseTimeseriesThresholdsOutput,
    # TimeseriesThresholds,
)
from talk_with_wiski.tools import get_locations as get_locations_pydantic_ai
from talk_with_wiski.tools import get_parameters as get_parameters_pydantic_ai
from talk_with_wiski.tools import get_group_list as get_group_list_pydantic_ai
from talk_with_wiski.tools import get_sites as get_sites_pydantic_ai
from talk_with_wiski.tools import get_timeseries_list as get_timeseries_list_pydantic_ai
from talk_with_wiski.tools import (
    get_timeseries_values as get_timeseries_values_pydantic_ai,
)
from talk_with_wiski.tools import (
    get_timeseries_type as get_timeseries_type_pydantic_ai,
)
from talk_with_wiski.tools import (
    get_parametertype_list as get_parametertype_list_pydantic_ai,
)
from talk_with_wiski.tools import (
    analyse_timeseries_statistics as get_analyse_timeseries_statistics_pydantic_ai,
)
from talk_with_wiski.tools import (
    analyse_timeseries_thresholds as get_analyse_timeseries_thresholds_pydantic_ai,
)
from talk_with_wiski.tools import (
    analyse_timeseries_trend as get_analyse_timeseries_trend_pydantic_ai,
)

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
    ctx = get_runtime_ctx()
    return await get_locations_pydantic_ai(ctx, input)


@mcp.tool()
@router.post("/tools/get_parameters")
@auto_docstring("Retrieves the parameters from the WISKI API")
async def get_parameters(
    input: GetParametersInput,
) -> GetParametersOutput:
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
    ctx = get_runtime_ctx()
    return await get_group_list_pydantic_ai(ctx, input)


@mcp.tool()
@router.post("/tools/get_parametertype_list")
@auto_docstring("Retrieves the parametertype list from the WISKI API")
async def get_parametertype_list(
    input: GetParametertypeListInput,
) -> GetParametertypeListOutput:
    ctx = get_runtime_ctx()
    return await get_parametertype_list_pydantic_ai(ctx, input)


@mcp.tool()
@router.post("/tools/get_timeseries_list")
@auto_docstring("Retrieves the available timeseries from the WISKI API")
async def get_timeseries_list(
    input: GetTimeseriesListInput,
) -> GetTimeseriesListOutput:
    ctx = get_runtime_ctx()
    return await get_timeseries_list_pydantic_ai(ctx, input)


@mcp.tool()
@router.post("/tools/get_timeseries_type")
@auto_docstring("Retrieves the timeseries data from the WISKI API")
async def get_timeseries_type(
    input: GetTimeseriesTypeInput,
) -> GetTimeseriesTypeOutput:
    ctx = get_runtime_ctx()
    return await get_timeseries_type_pydantic_ai(ctx, input)


@mcp.tool()
@router.post("/tools/get_timeseries_values")
@auto_docstring(
    "Retrieves the timeseries data from the WISKI API"
    "Note 1: Increase the parameter max_number_of_tsids_to_retrieve to retrieve more timeseries (default=5)."
    "Note 2: Increase the parameter max_number_of_values_per_tsid to retrieve more values per timeseries (default=10)."
)
async def get_timeseries_values(
    input: GetTimeseriesValuesInput,
) -> GetTimeseriesValuesOutput:
    ctx = get_runtime_ctx()
    return await get_timeseries_values_pydantic_ai(ctx, input)


@mcp.tool()
@router.post("/tools/analyse_timeseries_statistics")
@auto_docstring(
    "Analyse timeseries for a specific ts_id, get min/max/average/stddev"
    "Note 1: Increase the parameter max_number_of_tsids_to_retrieve to retrieve more timeseries (default=5)."
    "Note 2: Increase the parameter max_number_of_values_per_tsid to retrieve more values per timeseries (default=10)."
)
async def analyse_timeseries_statistics(
    input: AnalyseTimeseriesStatsInput,
) -> AnalyseTimeseriesStatsOutput:
    ctx = get_runtime_ctx()
    return await get_analyse_timeseries_statistics_pydantic_ai(ctx, input)


@mcp.tool()
@router.post("/tools/analyse_timeseries_thresholds")
@auto_docstring(
    "Analyse timeseries for a specific ts_id, get time in hours above a certain threshold"
    "Note 1: Increase the parameter max_number_of_tsids_to_retrieve to retrieve more timeseries (default=5)."
    "Note 2: Increase the parameter max_number_of_values_per_tsid to retrieve more values per timeseries (default=10)."
)
async def analyse_timeseries_thresholds(
    input: AnalyseTimeseriesThresholdsInput,
) -> AnalyseTimeseriesThresholdsOutput:
    ctx = get_runtime_ctx()
    return await get_analyse_timeseries_thresholds_pydantic_ai(ctx, input)


@mcp.tool()
@router.post("/tools/analyse_timeseries_trend")
@auto_docstring(
    "Analyse timeseries for a specific ts_id, get trend information"
    "Note 1: Increase the parameter max_number_of_tsids_to_retrieve to retrieve more timeseries (default=5)."
    "Note 2: Increase the parameter max_number_of_values_per_tsid to retrieve more values per timeseries (default=10)."
)
async def analyse_timeseries_trend(
    input: AnalyseTimeseriesTrendInput,
) -> AnalyseTimeseriesTrendOutput:
    ctx = get_runtime_ctx()
    return await get_analyse_timeseries_trend_pydantic_ai(ctx, input)
