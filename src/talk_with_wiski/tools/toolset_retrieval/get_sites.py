"""
Tool to getStationList from KiWIS API
Different parameters can be specified to build the getrequest string
"""

import json
import requests
from talk_with_wiski.models.modelset_retrieval.get_sites import (
    GetSitesInput,
    GetSitesOutput,
)
from talk_with_wiski.utils.logging_utils import log_tool_call
from talk_with_wiski.utils.logging_utils import logger
from geopy.distance import distance


def calculate_bbox_from_geocoding(lon, lat, r=5):
    """Return (xmin, ymin, xmax, ymax) around a point [lon, lat] within r km."""
    """Default radius is 5 [km], not that geolocator is not perfectly accurate in NL?!"""
    return [
        distance(kilometers=r).destination((lat, lon), 270).longitude,  # xmin (west)
        distance(kilometers=r).destination((lat, lon), 180).latitude,  # ymin (south)
        distance(kilometers=r).destination((lat, lon), 90).longitude,  # xmax (east)
        distance(kilometers=r).destination((lat, lon), 0).latitude,  # ymax (north)
    ]


@log_tool_call
async def get_sites(ctx, input: GetSitesInput) -> GetSitesOutput:
    """
    get_Sites from WISKI.
    input.site_no:   list of site_names
    input.site_id:   list of site_ids
    input.returnfields: string of returnfields
    input.bbox:         list of 4 floats defining bbox in lon/lat
    # bbox werkt niet op sites!!!
    input.max...:       maximum number of site_ids to return
    """
    #  you can access any context added to the ctx: Deps object
    ctx.deps.cache_database_db
    url = ctx.deps.url

    # base url
    endpoint = (
        url
        + "KiWIS?datasource=0&service=kisters&type=queryServices&request=getSiteList&format=objson"
    )

    # extend url
    if getattr(input, "returnfields", None):
        endpoint += "&returnfields=" + input.returnfields

    if getattr(input, "site_id", None):
        endpoint += "&site_id=" + ",".join(map(str, input.site_id))

    if getattr(input, "site_no", None):
        endpoint += "&site_no=" + ",".join(map(str, input.site_no))

    # API zou het wel moeten ondersteunen, maar lijkt niet te werken.
    # if getattr(input, "bbox", None):
    #     endpoint += "&bbox=" + ",".join(map(str, input.bbox))
    # if getattr(input, "requested_geolocation", None):
    #     from geopy.geocoders import Nominatim
    #     geolocator = Nominatim(user_agent="talk-with-wiski-notebook")
    #     print(input.requested_geolocation)
    #     location, radius = input.requested_geolocation
    #     radius=float(radius)
    #     geo_location = geolocator.geocode(location)
    #     print(geo_location)
    #     #print((geo_location.longitude, geo_location.latitude))
    #     loc_bbox=calculate_bbox_from_geocoding(
    #         geo_location.longitude,
    #         geo_location.latitude,
    #         r=radius
    #     )
    #     print(loc_bbox)
    #     endpoint += "&bbox=" + ",".join(map(str, loc_bbox))

    # filter on WSBDstations by default
    # dit moet alleen voor stations, niet voor sites
    # endpoint += "&object_type_shortname=WSBD_*"

    # For debugging
    # print(endpoint)

    # call to KiWIS API
    res = requests.get(endpoint)
    # maak er een json object van om terug te geven (default)
    data = list(json.loads(res.text))

    # get unique site_ids
    unique_ids = {
        item.get("site_id") for item in data if item.get("site_id") is not None
    }
    unique_ids = sorted(list(unique_ids))
    logger.debug("unique site_ids:", unique_ids)
    logger.debug("unique count:", len(unique_ids))

    Nstats = 5  # default: max 5 sites_ids teruggeven, tenzij gebruiker dit overschrijft
    if getattr(input, "max_number_of_site_ids", None):
        Nstats = input.max_number_of_site_ids
    # first N sorted site_ids
    firstN_site_ids = unique_ids[:Nstats]
    logger.debug("firstN site_ids:", firstN_site_ids)

    # filter data to only items that belong to these top5 site_ids
    filtered_data = [item for item in data if item.get("site_id") in firstN_site_ids]

    logger.debug("filtered count:", len(filtered_data))

    return GetSitesOutput(data=filtered_data, description="Data from KiWIS API")
