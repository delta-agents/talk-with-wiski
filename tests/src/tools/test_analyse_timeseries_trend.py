import os
import pytest


# to do trend analysis
from talk_with_wiski.tools.toolset_analysis.analyse_timeseries_trend import analyse_timeseries_trend
from talk_with_wiski.models.modelset_analysis.analyse_timeseries_trend import (
    AnalyseTimeseriesTrendInput,
    AnalyseTimeseriesTrendOutput,
    LinearTrendLine,
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
async def test_analyse_timeseries_trend(test_context):
    """Test for List of ts_ids"""
    # Test end time before start time
    input = AnalyseTimeseriesTrendInput(
        ts_id="37481042", # belongs to stat_no "1198_WTH_BOV"
        from_date="2023-11-01",
        period="P3M",  # dit mag niet icm from_date.. to_date
        number_of_tsids_to_retrieve=20,
        number_of_values_per_tsid=1000000,
    )

    output: AnalyseTimeseriesTrendOutput = await analyse_timeseries_trend(test_context, input)

    data = output.model_dump()
    #print(data)
    #print(type(data))
    #print(type(output))
    logger.debug(type(output))
    
    assert isinstance(output.linear_trend_line.slope, float)
    assert isinstance(output.linear_trend_line.intercept, float)
