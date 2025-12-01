from pydantic import Field
from typing import Dict, List, Optional

from talk_with_wiski.models.base import WiskiBaseModel


class GetSitesInput(WiskiBaseModel):
    """
    Input model for get_sites tool.
    """

    site_no: Optional[List[str]] = Field(
        default=None,
        description="Name of station (station_no). Total to return smaller than 5"
        "List of 1 or more, * as wildcard is allowed.",
    )
    site_id: Optional[List[int]] = Field(
        default=None,
        description="Index to use (station_id) in the example tool. Total to return smaller than 5",
    )
    max_number_of_site_ids: Optional[int] = Field(
        default=None,
        description="Index to use (station_id) in the example tool. Total to return smaller than 5",
    )
    returnfields: Optional[str] = Field(
        default="site_no,site_id,site_uuid,site_name,site_longname,site_latitude,site_longitude,site_type_name,site_type_shortname",
        description="Returnfields from API as string",
    )

    # DEZE WERKEN NIET OP sites (wel op stations)
    # requested_geolocation: Optional[List[str | float]] = Field(
    #     default=None,
    #     description="Requested geolocation for geocoding to a certain location in lon/lat, stations are searched within radius of geoloc (e.g. [Breda, 5.0])",
    # )
    # bbox: Optional[List[float]] = Field(default=None, description="bbox to clip data")

    # def validate_bbox():
    #  > 4.1 < 8.4
    #  > 50 < 54


class GetSitesOutput(WiskiBaseModel):
    """
    Output model for get_sites tool.
    """

    data: List[Dict[str, str]] = Field(..., description="data dictionary")
    description: str = Field(..., description="Table relationships")
