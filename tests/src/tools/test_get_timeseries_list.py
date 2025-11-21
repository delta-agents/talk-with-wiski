import os
import pytest
import json

from talk_with_wiski.tools import get_timeseries_list
from talk_with_wiski.models.modelset_retrieval.get_timeseries_list import (
    GetTimeseriesListInput,
    GetTimeseriesListOutput,
)
from talk_with_wiski.routers.setup_connections import get_runtime_ctx

from tests.utils_tests import setup_dot_env
from talk_with_wiski.utils.logging_utils import logger


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
async def test_get_timeseries_list(test_context):
    """Test handling timeseries list"""
    input = GetTimeseriesListInput(
        station_no="BRE0301_PMP1",
        parametertype_name=["WNS918", "WNS11872", "WNS9030"],
    )
    output: GetTimeseriesListOutput = await get_timeseries_list(test_context, input)

    unique_station_no = {
        item.get("station_no")
        for item in output.data
        if item.get("station_no") is not None
    }
    unique_parametertype_name = {
        item.get("parametertype_name")
        for item in output.data
        if item.get("parametertype_name") is not None
    }

    logger.debug(unique_station_no)
    logger.debug(unique_parametertype_name)

    assert len(unique_station_no) == 1
    assert len(unique_parametertype_name) == 3

    input = GetTimeseriesListInput(
        parametertype_name="WNS8487",  # dit is waterhoogte
        station_no="1198_WTH_BOV",  # dit is een station_no voor maken interessant figuur
        station_name="Bovenstrooms",  # dit is de naam van het station
    )
    output: GetTimeseriesListOutput = await get_timeseries_list(test_context, input)

    for i, item in enumerate(output.data):
        logger.debug(f"Item {i}:")
        logger.debug(json.dumps(item, indent=2, ensure_ascii=False))
