import pytest
import asyncio

from talk_with_wiski.routers.setup_connections import get_runtime_ctx
from talk_with_wiski.models.modelset_retrieval.get_locations import (
    GetLocationsInput,
    GetLocationsOutput,
)
from talk_with_wiski.tools.toolset_retrieval.get_locations import get_locations
from tests.utils_tests import setup_dot_env


@pytest.fixture
def test_context():
    """Create a test context with FEWS webservice URL"""
    setup_dot_env()
    return get_runtime_ctx()


@pytest.mark.asyncio
async def test_getlocations_by_station_id_list(test_context):
    """Get station name for (max 5) locations with a certain station_id"""
    # Get station name for (max 5) locations with a certain station_id
    # station_id is a list of integers. Length can 1...N, but is maximized 5 elements in get_locations unless user overrides this max
    # output is data from KiWIS API
    # Available return fields:
    #   station_no,station_id,station_name,station_latitude,station_longitude,site_id,site_name,parametertype_id,stationparameter_name,stationparameter_id,object_type,object_type_shortname
    # Default returnfields: only station_name

    print("Test 1 stations, all relevant returnfields")
    input = GetLocationsInput(station_id=[56620, 68870])
    output: GetLocationsOutput = await get_locations(test_context, input)
    print(output.data)
    print(len(output.data))
    print("\n")

    print("Test 2 station")
    input = GetLocationsInput(
        station_id=[56620], returnfields="station_id,station_name"
    )
    output: GetLocationsOutput = await get_locations(test_context, input)
    print(output.data)
    print(len(output.data))
    print("\n")

    print("Test 3 stations")
    input = GetLocationsInput(
        station_id=[56620, 68870], returnfields="station_id,station_name"
    )
    output: GetLocationsOutput = await get_locations(test_context, input)
    print(output.data)
    print(len(output.data))
    print("\n")


@pytest.mark.asyncio
async def test_getlocations_by_bbox(test_context):
    """Same as above, but now using a bbox"""
    # Same as above, but now using a bbox

    print("Test 4 stations, using a bbox, return only station_name")
    # test voor 'Loon op Zand', antwoord zou 100 locaties moeten zijn
    # &crs=global&bbox=5.053676588980831,51.61540080594861,5.096864369453537,51.635290829498146

    input = GetLocationsInput(
        bbox=[
            5.053676588980831,
            51.61540080594861,
            5.096864369453537,
            51.635290829498146,
        ],
        returnfields="station_id,station_name",
    )
    output: GetLocationsOutput = await get_locations(test_context, input)
    # print(output.data)
    print(len(output.data))
    print("\n")

    input = GetLocationsInput(
        bbox=[
            5.053676588980831,
            51.61540080594861,
            5.096864369453537,
            51.635290829498146,
        ],
        returnfields="station_id,station_name",
        max_number_of_station_ids=7,
    )
    output: GetLocationsOutput = await get_locations(test_context, input)
    print(output.data)
    # assert len(output.data)==7
    print(len(output.data))
    print("\n")


if __name__ == "__main__":
    asyncio.run(test_getlocations_by_station_id_list(test_context()))
    asyncio.run(test_getlocations_by_bbox(test_context()))
