import os
import pytest
import pandas as pd

# to do trend analysis
from talk_with_wiski.tools.toolset_analysis.analyse_timeseries_availability import (
    analyse_timeseries_availability,
)
from talk_with_wiski.models.modelset_analysis.analyse_timeseries_availability import (
    AnalyseTimeseriesAvailabilityInput,
    AnalyseTimeseriesAvailabilityOutput,
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
async def test_analyse_timeseries_availability_case_true(test_context):
    input = AnalyseTimeseriesAvailabilityInput(
        ts_id="63158042",  # belongs to stat_no="BRE0301_PMP1", parametertype_name="WNS11872"
        from_date="2023-11-01",
        period="P3M",
    )

    output: AnalyseTimeseriesAvailabilityOutput = await analyse_timeseries_availability(
        test_context, input
    )

    logger.debug(type(output))
    logger.debug(f"available = {output.available}")
    logger.debug(f"Tmin = {output.Tmin}")
    logger.debug(f"Tmax = {output.Tmax}")

    assert output.available
    assert output.Tmin is None


@pytest.mark.skipif(
    os.getenv("GITHUB_ACTIONS") == "true",
    reason="Kan alleen lokaal getest worden",
)
@pytest.mark.asyncio
async def test_analyse_timeseries_availability_case_false(test_context):
    input = AnalyseTimeseriesAvailabilityInput(
        ts_id="63158042",  # belongs to stat_no="BRE0301_PMP1", parametertype_name="WNS11872"
        from_date="2000-11-01",
        period="P1H",
    )

    output: AnalyseTimeseriesAvailabilityOutput = await analyse_timeseries_availability(
        test_context, input
    )

    logger.debug(type(output))
    logger.debug(f"available = {output.available}")
    logger.debug(f"Tmin = {output.Tmin}")
    logger.debug(f"Tmax = {output.Tmax}")

    assert not output.available
    assert type(output.Tmin) is pd.Timestamp
    assert type(output.Tmax) is pd.Timestamp
