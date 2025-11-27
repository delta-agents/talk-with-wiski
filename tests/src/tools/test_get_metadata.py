import os
import pytest

from talk_with_wiski.tools import get_metadata
from talk_with_wiski.models.modelset_retrieval.get_metadata import (
    GetMetadataInput,
    GetMetadataOutput,
)
from talk_with_wiski.routers.setup_connections import get_runtime_ctx

from tests.utils_tests import setup_dot_env
from talk_with_wiski.utils import logger


ts_id_list = [
    "5081042",
    "8936042",
    "5234042",
    "2993042",
    "31009042",
    "48392042",
    "2174042",
    "30588042",
    "70643042",
    "4441042",
    "52994042",
    "61944042",
    "60504042",
    "81555042",
    "4306042",
    "61749042",
    "8608042",
    "21670042",
    "32869042",
    "87482042",
    "4116042",
    "4754042",
    "329042",
    "3564042",
    "120042",
    "8602042",
    "93950042",
    "7830042",
    "21507042",
    "37534042",
    "94296042",
    "37621042",
    "1351042",
    "2150042",
    "62265042",
    "37420042",
    "62145042",
    "4516042",
    "85766042",
    "80702042",
    "2269042",
    "59847042",
    "2327042",
    "87041042",
    "4110042",
    "5548042",
    "3667042",
    "25906042",
    "30628042",
    "8913042",
    "8626042",
    "52713042",
    "8155042",
    "69035042",
    "3329042",
    "58483042",
    "87910042",
    "86243042",
    "4783042",
]


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
async def test_get_metadata(test_context):
    """Test handling timeseries metadata"""
    input = GetMetadataInput(
        ts_id=ts_id_list,
    )
    ts_metadata_list_of_dicts: GetMetadataOutput = await get_metadata(
        test_context, input
    )

    logger.debug(ts_metadata_list_of_dicts.data[0])

    # Extract site_no values from the metadata
    site_no_list = [item["site_no"] for item in ts_metadata_list_of_dicts.data]
    logger.debug(f"sites: {site_no_list}")

    # Extract site_no values from the metadata
    station_no_list = [item["station_no"] for item in ts_metadata_list_of_dicts.data]
    logger.debug(f"stations: {station_no_list}")

    input = GetMetadataInput(
        site_no=site_no_list,
    )
    site_metadata_list_of_dicts: GetMetadataOutput = await get_metadata(
        test_context, input
    )
    logger.debug(site_metadata_list_of_dicts.data)

    input = GetMetadataInput(
        station_no=station_no_list,
    )
    station_metadata_list_of_dicts: GetMetadataOutput = await get_metadata(
        test_context, input
    )
    logger.debug(station_metadata_list_of_dicts.data)

    # Voorbeeld voor koppelen van twee tabellen metadata (site_no based)
    merged_list = [
        {**d1, **d2}
        for d1 in ts_metadata_list_of_dicts.data
        for d2 in site_metadata_list_of_dicts.data
        if d1["site_no"] == d2["site_no"]
    ]
    # logger.debug(merged_list[0])

    # logger.debug(len(ts_id_list), len(site_no_list), len(merged_list))
    assert len(ts_id_list) == len(site_no_list) == len(merged_list)
