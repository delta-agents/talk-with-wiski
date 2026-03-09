from fastapi import APIRouter
from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier

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
    GetMetadataInput,
    GetMetadataOutput,
    GetQualityCodeTableInput,
    GetQualityCodeTableOutput,
    AnalyseTimeseriesTrendInput,
    AnalyseTimeseriesTrendOutput,
    # LinearTrendLine,
    AnalyseTimeseriesStatsInput,
    AnalyseTimeseriesStatsOutput,
    # TimeseriesStatistics,
    AnalyseTimeseriesThresholdsInput,
    AnalyseTimeseriesThresholdsOutput,
    # TimeseriesThresholds,
    AnalyseTimeseriesQualityCodeInput,
    AnalyseTimeseriesQualityCodeOutput,
    AnalyseTimeseriesAvailabilityInput,
    AnalyseTimeseriesAvailabilityOutput,
    GetCurrentTimeInput,
    GetCurrentTimeOutput,
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
    get_metadata as get_metadata_pydantic_ai,
)
from talk_with_wiski.tools import (
    get_quality_code_table as get_quality_code_table_pydantic_ai,
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
from talk_with_wiski.tools import (
    analyse_timeseries_quality_code as get_analyse_timeseries_quality_code_pydantic_ai,
)
from talk_with_wiski.tools import (
    analyse_timeseries_availability as get_analyse_timeseries_availability_pydantic_ai,
)

from talk_with_wiski.tools import get_current_time as get_current_time_pydantic_ai


# Import tool functions and their models
from talk_with_wiski.routers.setup_connections import get_runtime_ctx, get_user_settings, setup_env

tokens = setup_env()
verifier = StaticTokenVerifier(tokens=tokens, required_scopes=["read:data"])

router = APIRouter()
mcp = FastMCP(name="Wiski", auth=verifier)


# describe_timeseries tool registration
@mcp.tool()
@router.post("/tools/get_locations")
@auto_docstring(
    "Retrieves the locations from the WISKI API. May contain * as wildcard for some parameters"
)
async def get_locations(
    input: GetLocationsInput,
) -> GetLocationsOutput:
    user_settings: dict = get_user_settings(verifier)
    ctx = get_runtime_ctx(user_settings)
    return await get_locations_pydantic_ai(ctx, input)


@mcp.tool()
@router.post("/tools/get_parameters")
@auto_docstring("Retrieves the parameters from the WISKI API")
async def get_parameters(
    input: GetParametersInput,
) -> GetParametersOutput:
    user_settings: dict = get_user_settings(verifier)
    ctx = get_runtime_ctx(user_settings)
    return await get_parameters_pydantic_ai(ctx, input)


@mcp.tool()
@router.post("/tools/get_sites")
@auto_docstring(
    "Retrieves the sites information from the WISKI API. May contain * as wildcard for some parameters"
)
async def get_sites(
    input: GetSitesInput,
) -> GetSitesOutput:
    user_settings: dict = get_user_settings(verifier)
    ctx = get_runtime_ctx(user_settings)
    return await get_sites_pydantic_ai(ctx, input)


@mcp.tool()
@router.post("/tools/get_group_list")
@auto_docstring(
    "Retrieves the group list from the WISKI API. May contain * as wildcard for some parameters"
)
async def get_group_list(
    input: GetGroupListInput,
) -> GetGroupListOutput:
    user_settings: dict = get_user_settings(verifier)
    ctx = get_runtime_ctx(user_settings)
    return await get_group_list_pydantic_ai(ctx, input)


@mcp.tool()
@router.post("/tools/get_parametertype_list")
@auto_docstring(
    "Retrieves the parametertype list from the WISKI API. May contain * as wildcard for some parameters"
)
async def get_parametertype_list(
    input: GetParametertypeListInput,
) -> GetParametertypeListOutput:
    user_settings: dict = get_user_settings(verifier)
    ctx = get_runtime_ctx(user_settings)
    return await get_parametertype_list_pydantic_ai(ctx, input)


@mcp.tool()
@router.post("/tools/get_metadata")
@auto_docstring(
    "Retrieves metadata from the WISKI API, input can be (str of List[str]) of either ts_id, site_no or station_no"
)
async def get_metadata(
    input: GetMetadataInput,
) -> GetMetadataOutput:
    user_settings: dict = get_user_settings(verifier)
    ctx = get_runtime_ctx(user_settings)
    return await get_metadata_pydantic_ai(ctx, input)


@mcp.tool()
@router.post("/tools/get_quality_code_table")
@auto_docstring("Dictionary of quality codes from the WISKI API")
async def get_quality_code_table(
    input: GetQualityCodeTableInput,
) -> GetQualityCodeTableOutput:
    user_settings: dict = get_user_settings(verifier)
    ctx = get_runtime_ctx(user_settings)
    return await get_quality_code_table_pydantic_ai(ctx, input)


@mcp.tool()
@router.post("/tools/get_timeseries_list")
@auto_docstring(
    "Retrieves the available timeseries from the WISKI API. May contain * as wildcard for some parameters"
)
async def get_timeseries_list(
    input: GetTimeseriesListInput,
) -> GetTimeseriesListOutput:
    user_settings: dict = get_user_settings(verifier)
    ctx = get_runtime_ctx(user_settings)
    return await get_timeseries_list_pydantic_ai(ctx, input)


@mcp.tool()
@router.post("/tools/get_timeseries_type")
@auto_docstring("Retrieves the timeseries data from the WISKI API")
async def get_timeseries_type(
    input: GetTimeseriesTypeInput,
) -> GetTimeseriesTypeOutput:
    user_settings: dict = get_user_settings(verifier)
    ctx = get_runtime_ctx(user_settings)
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
    user_settings: dict = get_user_settings(verifier)
    ctx = get_runtime_ctx(user_settings)
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
    user_settings: dict = get_user_settings(verifier)
    ctx = get_runtime_ctx(user_settings)
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
    user_settings: dict = get_user_settings(verifier)
    ctx = get_runtime_ctx(user_settings)
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
    user_settings: dict = get_user_settings(verifier)
    ctx = get_runtime_ctx(user_settings)
    return await get_analyse_timeseries_trend_pydantic_ai(ctx, input)


@mcp.tool()
@router.post("/tools/analyse_timeseries_availability")
@auto_docstring("Analyse timeseries for a specific ts_id, get availability information")
async def analyse_timeseries_availability(
    input: AnalyseTimeseriesAvailabilityInput,
) -> AnalyseTimeseriesAvailabilityOutput:
    user_settings: dict = get_user_settings(verifier)
    ctx = get_runtime_ctx(user_settings)
    return await get_analyse_timeseries_availability_pydantic_ai(ctx, input)


@mcp.tool()
@router.post("/tools/analyse_timeseries_quality_code")
@auto_docstring(
    "Analyse timeseries for a specific ts_id, get quality code information"
    "Note 1: Increase the parameter max_number_of_tsids_to_retrieve to retrieve more timeseries (default=5)."
    "Note 2: Increase the parameter max_number_of_values_per_tsid to retrieve more values per timeseries (default=10)."
)
async def analyse_timeseries_quality_code(
    input: AnalyseTimeseriesQualityCodeInput,
) -> AnalyseTimeseriesQualityCodeOutput:
    user_settings: dict = get_user_settings(verifier)
    ctx = get_runtime_ctx(user_settings)
    return await get_analyse_timeseries_quality_code_pydantic_ai(ctx, input)


@mcp.tool()
@router.post("/tools/get_current_time")
@auto_docstring(
    "ALWAYS CALL BEFORE ANY OTHER TOOL: Return the current time as ISO formatted string"
)
async def get_current_time(
    input: GetCurrentTimeInput,
) -> GetCurrentTimeOutput:
    user_settings: dict = get_user_settings(verifier)
    ctx = get_runtime_ctx(user_settings)
    return await get_current_time_pydantic_ai(ctx, input)
