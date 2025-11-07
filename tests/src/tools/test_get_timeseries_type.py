import os
import pytest


from talk_with_wiski.tools import get_timeseries_type
from talk_with_wiski.models.modelset_retrieval.get_timeseries_type import (
    GetTimeseriesTypeInput,
    GetTimeseriesTypeOutput,
)
from talk_with_wiski.routers.setup_connections import get_runtime_ctx

from tests.utils_tests import setup_dot_env


@pytest.fixture
def test_context():
    """Create a test context with FEWS webservice URL"""
    setup_dot_env()
    return get_runtime_ctx()


@pytest.mark.skipif(
    os.getenv("GITHUB_ACTIONS") == "true",
    reason="Kan alleen lokaal getest worden",
)
@pytest.mark.asyncio
async def test_get_timeseries_type_default(test_context):
    """Test handling of invalid time ranges"""
    # Test end time before start time
    input = GetTimeseriesTypeInput(ts_type_id=12042)
    output: GetTimeseriesTypeOutput = await get_timeseries_type(test_context, input)

    assert len(output.timeseries_type_list) == 3
    assert "Only the first" not in output.description


@pytest.mark.skipif(
    os.getenv("GITHUB_ACTIONS") == "true",
    reason="Kan alleen lokaal getest worden",
)
@pytest.mark.asyncio
async def test_get_timeseries_type_by_name_10(test_context):
    """Test handling of invalid time ranges"""
    # Test end time before start time
    input = GetTimeseriesTypeInput(
        ts_shortname="Year.Min", number_of_timeseries_types=10
    )

    output: GetTimeseriesTypeOutput = await get_timeseries_type(test_context, input)

    assert len(output.timeseries_type_list) == 1
