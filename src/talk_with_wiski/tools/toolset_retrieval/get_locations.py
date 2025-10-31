"""
Tool to getStationList from KiWIS API
Different parameters can be specified to build the getrequest string
"""

import json
import requests
from talk_with_wiski.models.modelset_retrieval.get_locations import (
    GetLocationsInput,
    GetLocationsOutput,
)
from talk_with_wiski.utils.logging_utils import log_tool_call
from talk_with_wiski.utils.logging_utils import logger
from geopy.distance import distance


def calculate_bbox_from_geocoding(lon, lat, r=5):
    """Return (xmin, ymin, xmax, ymax) around a point [lon, lat] within r km."""
    """Default radius is 5 [km], note that geolocator is not perfectly accurate in NL?!"""
    """Radius is a float in km"""
    return [
        distance(kilometers=r).destination((lat, lon), 270).longitude,  # xmin (west)
        distance(kilometers=r).destination((lat, lon), 180).latitude,   # ymin (south)
        distance(kilometers=r).destination((lat, lon), 90).longitude,   # xmax (east)
        distance(kilometers=r).destination((lat, lon), 0).latitude      # ymax (north)
    ]

@log_tool_call
async def get_locations(ctx, input: GetLocationsInput) -> GetLocationsOutput:
    """
    get_locations from WISKI.
    input.station_no:   list of station_names
    input.station_id:   list of station_ids
    input.returnfields: string of returnfields
    input.bbox:         list of 4 floats defining bbox in lon/lat
    input.max...:       maximum number of station_ids to return
    """
    #  you can access any context added to the ctx: Deps object
    ctx.deps.cache_database_db
    url = ctx.deps.url

    # base url
    endpoint = (
        url
        + "KiWIS?datasource=0&service=kisters&type=queryServices&request=getStationList&format=objson"
    )

    # extend url
    if getattr(input, "returnfields", None):
        endpoint += "&returnfields=" + input.returnfields

    if getattr(input, "station_id", None):
        endpoint += "&station_id=" + ",".join(map(str, input.station_id))

    if getattr(input, "station_no", None):
        endpoint += "&station_no=" + ",".join(map(str, input.station_no))

    if getattr(input, "bbox", None):
        endpoint += "&bbox=" + ",".join(map(str, input.bbox))

    if getattr(input, "requested_geolocation", None):
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent="talk-with-wiski-notebook")
        # LET OP @@@
        logger.debug(input.requested_geolocation)
        location, radius = input.requested_geolocation
        radius=float(radius)
        geo_location = geolocator.geocode(location)
        logger.debug(geo_location)
        #print((geo_location.longitude, geo_location.latitude))
        loc_bbox=calculate_bbox_from_geocoding(
            geo_location.longitude,
            geo_location.latitude,
            r=radius
        )
        logger.debug(loc_bbox)
        endpoint += "&bbox=" + ",".join(map(str, loc_bbox))

    # filter on WSBDstations by default
    endpoint += "&object_type_shortname=WSBD_*"

    # For debugging
    logger.debug(endpoint)
    logger.debug('\n'.join(endpoint.split('&')))

    # call to KiWIS API
    res = requests.get(endpoint)
    # maak er een json object van om terug te geven (default)
    data = list(json.loads(res.text))

    # get unique station_ids
    unique_ids = {
        item.get("station_id") for item in data if item.get("station_id") is not None
    }
    unique_ids = sorted(list(unique_ids))
    logger.debug("unique station_ids:", unique_ids)
    logger.debug("unique count:", len(unique_ids))

    Nstats = 5  # default: max 5 stations teruggeven, tenzij gebruiker dit overschrijft
    if getattr(input, "max_number_of_station_ids", None):
        Nstats = input.max_number_of_station_ids
    # first N sorted station_ids
    firstN_station_ids = unique_ids[:Nstats]
    logger.debug("firstN station_ids:", firstN_station_ids)

    # filter data to only items that belong to these top5 station_ids
    filtered_data = [
        item for item in data if item.get("station_id") in firstN_station_ids
    ]

    logger.debug("filtered count:", len(filtered_data))

    return GetLocationsOutput(data=filtered_data, description="Data from KiWIS API")
