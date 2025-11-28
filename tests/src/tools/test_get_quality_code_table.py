import os
import pytest

from talk_with_wiski.tools import get_quality_code_table
from talk_with_wiski.models.modelset_retrieval.get_quality_code_table import (
    GetQualityCodeTableInput,
    GetQualityCodeTableOutput,
)
from talk_with_wiski.routers.setup_connections import get_runtime_ctx

from tests.utils_tests import setup_dot_env
from talk_with_wiski.utils import logger


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
async def test_get_quality_code_table(test_context):
    """Test handling timeseries metadata"""
    input = GetQualityCodeTableInput()
    quality_code_table: GetQualityCodeTableOutput = await get_quality_code_table(
        test_context, input
    )
    quality_code_table=quality_code_table.data

    logger.debug(quality_code_table)

    unique_count = len(quality_code_table)

    # 10 codes in table (needs needs to be updated if table in WISKI changes)
    # alternative: read from WISKI database
    assert unique_count == 10
