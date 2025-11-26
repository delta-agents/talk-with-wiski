import os
import pytest
import pandas as pd

# to do trend analysis
from talk_with_wiski.tools.toolset_analysis.analyse_timeseries_quality_code import (
    analyse_timeseries_quality_code,
)
from talk_with_wiski.models.modelset_analysis.analyse_timeseries_quality_code import (
    AnalyseTimeseriesQualityCodeInput,
    AnalyseTimeseriesQualityCodeOutput,
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
async def test_analyse_timeseries_quality_code(test_context):
    """Test for List of ts_ids"""
    # Test end time before start time
    input = AnalyseTimeseriesQualityCodeInput(
        ts_id=["37481042","63160042"],  # belongs to stat_no "1198_WTH_BOV"
        from_date="2023-11-01",
        period="P1D",  # dit mag niet icm from_date.. to_date
        #max_number_of_tsids_to_retrieve=20,
        #max_number_of_values_per_tsid=1000000,
    )

    output: AnalyseTimeseriesQualityCodeOutput = await analyse_timeseries_quality_code(
        test_context, input
    )

    logger.debug(type(output))
    df = pd.DataFrame(output.timeseries_quality_codes)
    logger.debug(df)

    # Find the index of the 'n_datapoints' column
    idx = df.columns.get_loc("n_datapoints")
    right_cols = df.columns[idx + 1:]
    # Row by row check
    # Row by row check: n_datapoints == sum of right_cols
    for i, row in df.iterrows():
        right_sum = row[right_cols].sum()
        assert row["n_datapoints"] == right_sum, (
            f"Row {i}: n_datapoints ({row['n_datapoints']}) != sum({list(right_cols)}) ({right_sum})"
        )
    