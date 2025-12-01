from pydantic import Field
from typing import Dict, List, Optional

from talk_with_wiski.models.base import WiskiBaseModel


class GetLocationsInput(WiskiBaseModel):
    """
    Input model for get_locations tool.
    """

    requested_geolocation: Optional[List[str | float]] = Field(
        default=None,
        description="Requested geolocation for geocoding to a certain location in lon/lat, stations are searched within radius of geoloc (e.g. [Breda, 5.0])",
    )
    station_no: Optional[List[str]] = Field(
        default=None,
        description="Name of station (station_no). Total to return smaller than 5"
        "List of 1 or more, * as wildcard is allowed.",
    )
    station_name: Optional[List[str]] = Field(
        default=None,
        description="Name of station (station_name). Total to return smaller than 5"
        "List of 1 or more, * as wildcard is allowed.",
    )
    station_id: Optional[List[int]] = Field(
        default=None,
        description="Index to use (station_id) in the example tool. Total to return smaller than 5",
    )
    max_number_of_station_ids: Optional[int] = Field(
        default=None,
        description="Maximum number is by default 5. If more required, increase this number",
        # default=10,  # verhoogd van None naar 10
        # description="Maximum number of station_ids to return (default: 10)",
        # ge=1,  # minimum value of 1
        # le=100  # maximum value of 100
    )
    returnfields: Optional[str] = Field(
        default="station_no,station_id,station_name,station_latitude,station_longitude,site_id,site_name,parametertype_id,stationparameter_name,stationparameter_id,object_type,object_type_shortname",
        description="Returnfields from API as string",
    )
    get_as_url: Optional[bool] = Field(
        default=False,
        description="Option to get url instead of data in case of large data requests",
    )
    bbox: Optional[List[float]] = Field(default=None, description="bbox to clip data")

    # def validate_bbox():
    #  > 4.1 < 8.4
    #  > 50 < 54


class GetLocationsOutput(WiskiBaseModel):
    data: List[Dict[str, str]] = Field(..., description="data dictionary")
    description: str = Field(..., description="Table relationships")
    url: str = Field(..., description="URL to retrieve large data sets")
