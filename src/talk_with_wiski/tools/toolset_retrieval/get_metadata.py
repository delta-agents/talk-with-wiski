"""
tool call to get metadata.
"""

from talk_with_wiski.models.modelset_retrieval.get_metadata import (
    GetMetadataInput,
    GetMetadataOutput,
)
from talk_with_wiski.utils.logging_utils import log_tool_call
import requests
import json

@log_tool_call
async def get_metadata(
    ctx, input: GetMetadataInput
) -> GetMetadataOutput:
    """
    Get metadata.
    """

    #  you can access any context added to the ctx: Deps object
    url = ctx.deps.url
    # base url
    endpoint = url + "KiWIS"
    params = {
        "datasource": "0",
        "service": "kisters",
        "type": "queryServices",
        "format": "objson",
    }

    # inputs used to extend url
    # input can only be ONE of ts_id, site_no, station_no (see model_validator)
    if input.ts_id is not None:
        # use request getTimeseriesList
        caseid='Timeseries'
        params["request"] = "getTimeseriesList"
        params["returnfields"] = "ts_id,site_no,station_no,catchment_id,ca_sta"
        if isinstance(input.ts_id, list):
            params["ts_id"] = ",".join(input.ts_id)
        else:
            params["ts_id"] = input.ts_id
    elif input.site_no is not None:
        # use request getSiteList
        caseid='Sites'
        params["request"] = "getSiteList"
        params["returnfields"] = "site_no,site_id,site_name,site_type_name,ca_site"
        if isinstance(input.site_no, list):
            params["site_no"] = ",".join(input.site_no)
        else:
            params["site_no"] = input.site_no
    elif input.station_no is not None:
        # use request getStationList
        caseid='Stations'
        params["request"] = "getStationList"
        params["returnfields"] = "station_no,object_type,object_type_shortname,river_id,river_name,area_id,area_name,ca_sta"
        if isinstance(input.station_no, list):
            params["station_no"] = ",".join(input.station_no)
        else:
            params["station_no"] = input.station_no

    # request data
    res = requests.get(endpoint, params=params, timeout=30)
    list_of_dicts = list(json.loads(res.text))    # dit is een list_of_dicts
    

    return GetMetadataOutput(
        data=list_of_dicts,
        description=f'Metadata for {caseid}',
    )
