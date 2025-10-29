from pydantic import BaseModel, Field
from typing import Dict, List, Optional

from talk_with_wiski.models.base import ExampleBaseModel


class GetLocationsInput(ExampleBaseModel):
    """
    Input model for Example1Input tool.
    Currently, no parameters are required, but this can be extended in the future.
    """

    station_id: Optional[List[int]] = Field(
        default=None,
        description="Index to use (station_id) in the example tool. Total to return smaller than 5",
    )
    max_number_of_station_ids: Optional[int] = Field(
        default=None,
        description="Index to use (station_id) in the example tool. Total to return smaller than 5",
    )
    returnfields: Optional[str] = Field(
        default="station_no,station_id,station_name,station_latitude,station_longitude,site_id,site_name,parametertype_id,stationparameter_name,stationparameter_id,object_type,object_type_shortname",
        description="Returnfields from API as string",
    )
    bbox: Optional[List[float]] = Field(default=None, description="bbox to clip data")

    # def validate_bbox():
    #  > 4.1 < 8.4
    #  > 50 < 54


class GetLocationsOutput(BaseModel):
    data: List[Dict[str, str]] = Field(..., description="data dictionary")
    description: str = Field(..., description="Table relationships")
