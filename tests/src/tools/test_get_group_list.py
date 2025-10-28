import os
import pytest


from talk_with_wiski.tools import get_group_list
from talk_with_wiski.models.modelset_retrieval.get_group_list import (
    GetGroupListInput,
    GetGroupListOutput,
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
async def test_get_group_list_default(test_context):
    """Test handling of invalid time ranges"""
    # Test end time before start time
    input = GetGroupListInput(group_type="timeseries")

    output: GetGroupListOutput = await get_group_list(test_context, input)

    assert len(output.group_item_list) == 5  # by default
    assert "Group list retrieved successfully" in output.description


@pytest.mark.skipif(
    os.getenv("GITHUB_ACTIONS") == "true",
    reason="Kan alleen lokaal getest worden",
)
@pytest.mark.asyncio
async def test_get_group_list_10(test_context):
    """Test handling of invalid time ranges"""
    # Test end time before start time
    input = GetGroupListInput(group_type="station", number_of_groups_retrieved=10)

    output: GetGroupListOutput = await get_group_list(test_context, input)

    assert len(output.group_item_list) == 10  # check if more is better
    assert "Group list retrieved successfully" in output.description
