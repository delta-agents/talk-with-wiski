import os
import pytest
import asyncio
import numpy as np

from talk_with_wiski.tools import get_parameters
from talk_with_wiski.models.modelset_retrieval.get_parameters import (
    GetParametersInput,
    GetParametersOutput,
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
async def test_get_parameters(test_context):

    #
    #
    """Test handling of list of station_no"""
    # TEST 1, voor lijst van stations stations
    logger.debug("Test 1: handling of list of station_no-s")
    input = GetParametersInput(station_no=["ZUN0034_KKL_OW", "0300_TDB"])
    output: GetParametersOutput = await get_parameters(test_context, input)
    # get unique station_no
    unique_station_no = {
        item.get("station_no") for item in output.data if item.get("station_no") is not None
    }
    #print(output.data)
    logger.debug(unique_station_no)
    assert len(unique_station_no) == 2

    #
    #
    """Test handling of list of station_no"""
    # TEST 2, voor lijst van stations stations
    logger.debug("Test 2: handling of station_no")
    input = GetParametersInput(station_no="BRE0301_PMP1")
    output: GetParametersOutput = await get_parameters(test_context, input)
    # get unique station_no
    unique_station_no = {
        item.get("station_no") for item in output.data if item.get("station_no") is not None
    }
    #print(output.data)
    logger.debug(unique_station_no)
    assert len(unique_station_no) == 1

    #
    #
    """Alle stations"""
    # TEST 3, alle stations
    logger.debug("Test 2: handling of station_no")
    input = GetParametersInput()
    output: GetParametersOutput = await get_parameters(test_context, input)
    # get unique station_no
    unique_station_no = {
        item.get("station_no") for item in output.data if item.get("station_no") is not None
    }
    data_dict = output.data
    parameters = np.unique(
        [row["stationparameter_longname"].split(" [")[0].lower() for row in data_dict]
    )
    logger.debug(parameters)

    logger.debug(unique_station_no)
    assert len(unique_station_no) > 0
    assert len(parameters) > 0
