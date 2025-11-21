import os
import pytest


# to do trend analysis
from talk_with_wiski.tools.toolset_analysis.analyse_timeseries_statistics import analyse_timeseries_statistics
from talk_with_wiski.models.modelset_analysis.analyse_timeseries_statistics import (
    AnalyseTimeseriesStatsInput,
    AnalyseTimeseriesStatsOutput,
    TimeseriesStatistics,
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
async def test_analyse_timeseries_statistics(test_context):
    """Test for List of ts_ids"""
    # Test end time before start time
    input = AnalyseTimeseriesStatsInput(
        ts_id="37481042", # belongs to stat_no "1198_WTH_BOV"
        from_date="2023-11-01",
        period="P3M",  # dit mag niet icm from_date.. to_date
        number_of_tsids_to_retrieve=20,
        number_of_values_per_tsid=1000000,
    )

    output: AnalyseTimeseriesStatsOutput = await analyse_timeseries_statistics(test_context, input)

    data = output.model_dump()
    logger.debug(type(output))
    
    #print('\n')
    logger.debug(f'maximum= {output.timeseries_statistics.maximum}')

    assert isinstance(output.timeseries_statistics.minimum, float)
    assert isinstance(output.timeseries_statistics.maximum, float)
    assert output.timeseries_statistics.maximum >= output.timeseries_statistics.minimum
