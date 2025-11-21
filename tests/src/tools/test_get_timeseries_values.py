import os
import pytest


from talk_with_wiski.tools import get_timeseries_values
from talk_with_wiski.models.modelset_retrieval.get_timeseries_values import (
    GetTimeseriesValuesInput,
    GetTimeseriesValuesOutput,
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
async def test_get_timeseries_values(test_context):
    """Test for List of ts_ids"""
    # Test end time before start time
    input = GetTimeseriesValuesInput(
        ts_id=["63158042", "63160042", "63162042"],
        from_date="2025-11-01",
        period="P10D",
        max_number_of_tsids_to_retrieve=10,
        max_number_of_values_per_tsid=60,
        get_as_url=True,
    )

    output: GetTimeseriesValuesOutput = await get_timeseries_values(test_context, input)

    if not input.get_as_url:
        # check on maximum number of ts_ids returned :
        assert (
            len(output.timeseries_values_list) <= input.max_number_of_tsids_to_retrieve
        )
        assert "Only the first" not in output.description

        logger.debug(output)
        logger.debug(
            f"Aantal tsids in output: {len(output.model_dump()['timeseries_values_list'])}"
        )

        data = output.model_dump()
        # print(type(data))

        for item in data["timeseries_values_list"]:
            ts_id = item["ts_id"]
            station = item["station_name"]
            data_length = len(item["data"])
            logger.debug(
                f"TS ID: {ts_id} | Station: {station} | Number of data points: {data_length}"
            )
            # check on maximum number of records per ts_id :
            assert data_length <= input.max_number_of_values_per_tsid

        logger.debug("\n")

    else:
        # output: str = await get_timeseries_values(test_context, input)
        # logger.debug(output)
        data = output.model_dump()
        logger.debug(data["url"])
        assert "KiWIS" in data["url"]
