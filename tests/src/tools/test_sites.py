import os
import pytest
import asyncio

from talk_with_wiski.routers.setup_connections import get_runtime_ctx
from talk_with_wiski.models.modelset_retrieval.get_sites import (
    GetSitesInput,
    GetSitesOutput,
)
from talk_with_wiski.tools.toolset_retrieval.get_sites import get_sites
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
async def test_getsites_by_site_id_list(test_context):
    """Get site name for (max 5) locations with a certain site_id"""
    logger.debug("Test 1: sites, all relevant returnfields")
    input = GetSitesInput(site_id=[48290, 115783])
    output: GetSitesOutput = await get_sites(test_context, input)
    logger.debug(output.data)
    logger.debug(len(output.data))
    logger.debug("\n")

    logger.debug("Test 2: single station, specific returnfields")
    input = GetSitesInput(site_id=[48290], returnfields="site_no,site_id,site_name")
    output: GetSitesOutput = await get_sites(test_context, input)
    logger.debug(output.data)
    logger.debug(len(output.data))
    logger.debug("\n")

    logger.debug("Test 3: combination")
    input = GetSitesInput(
        site_id=[48290, 115783], returnfields="site_no,site_id,site_name"
    )
    output: GetSitesOutput = await get_sites(test_context, input)
    logger.debug(output.data)
    logger.debug(len(output.data))
    logger.debug("\n")


if __name__ == "__main__":
    asyncio.run(test_getsites_by_site_id_list(test_context()))
