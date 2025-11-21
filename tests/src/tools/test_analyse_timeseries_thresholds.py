import os
import pytest


# to do trend analysis
from talk_with_wiski.tools.toolset_analysis.analyse_timeseries_thresholds import analyse_timeseries_thresholds
from talk_with_wiski.models.modelset_analysis.analyse_timeseries_thresholds import (
    AnalyseTimeseriesThresholdsInput,
    AnalyseTimeseriesThresholdsOutput,
    TimeseriesThresholds,
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
async def test_analyse_timeseries_thresholds(test_context):
    input = AnalyseTimeseriesThresholdsInput(
        ts_id="37481042", # belongs to stat_no "1198_WTH_BOV"
        from_date="2023-11-01",
        period="P3M",  # dit mag niet icm from_date.. to_date
        max_number_of_tsids_to_retrieve=20,
        max_number_of_values_per_tsid=1000000,
        threshold=5.3, # deze reeks ligt >0 uur boven deze threshold
    )

    output: AnalyseTimeseriesThresholdsOutput = await analyse_timeseries_thresholds(test_context, input)

    data = output.model_dump()
    logger.debug(type(output))
    
    #print('\n')
    logger.debug(f'threshold= {output.threshold_values.threshold_value} mNAP')
    logger.debug(f'total_time_above= {output.threshold_values.total_time_above_in_hours} hours')

    assert output.threshold_values.total_time_above_in_hours > 0.0

    input = AnalyseTimeseriesThresholdsInput(
        ts_id="37481042", # belongs to stat_no "1198_WTH_BOV"
        from_date="2023-11-01",
        period="P3M",  # dit mag niet icm from_date.. to_date
        number_of_tsids_to_retrieve=20,
        number_of_values_per_tsid=1000000,
        threshold=5.5, # gehele reeks ligt onder deze threshold, dus test op ==0
    )

    output: AnalyseTimeseriesThresholdsOutput = await analyse_timeseries_thresholds(test_context, input)

    data = output.model_dump()
    logger.debug(type(output))
    
    #print('\n')
    logger.debug(f'threshold= {output.threshold_values.threshold_value} mNAP')
    logger.debug(f'total_time_above= {output.threshold_values.total_time_above_in_hours} hours')

    assert output.threshold_values.total_time_above_in_hours == 0.0
