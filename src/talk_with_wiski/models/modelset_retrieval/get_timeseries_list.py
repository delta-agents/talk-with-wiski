from pydantic import BaseModel, Field, model_validator
from pydantic_ai import ModelRetry
from typing import Dict, List, Optional

from talk_with_wiski.models.base import ExampleBaseModel


class GetTimeseriesListInput(ExampleBaseModel):
    """
    Input model for get_timeseries_list tool.
    Currently, no parameters are required, but this can be extended in the future.
    """

    station_no: Optional[str | List[str]] = Field(
        default=None,
        description="Station number or numbers for which to list all available parameters. This variable can be obtained from GetLocationsOutput (the output of the function get_locations)",
    )
    station_name: Optional[str | List[str]] = Field(
        default=None,
        description="Station name or names for which to list all available parameters. This variable can be obtained from GetLocationsOutput (the output of the function get_locations)",
    )
    site_no: Optional[str | List[str]] = Field(
        default=None,
        description="Site number or numbers for which to list all available parameters. This variable can be obtained from GetSitesOutput (the output of the function get_sites)",
    )
    parametertype_name: Optional[str | List[str]] = Field(
        default=None,
        description="List all available parameters that feature the parameter type. This variable can be obtained from GetParametersOutput or GetParametertypeListOutput (the output of the function get_parameters or get_parametertype_list)",
    )

    @model_validator(mode="after")
    def validate_exclusive_fields(self):
        station_no, site_no, parametertype_name = (
            self.station_no,
            self.site_no,
            self.parametertype_name,
        )
        if station_no and site_no:
            raise ModelRetry(
                "Only one of 'station_no' or 'site_no' can be provided, not both."
            )
        elif not (station_no or site_no or parametertype_name):
            raise ModelRetry(
                "At least one of the arguments 'station_no', 'site_no', or 'parametertype_name' must be provided."
            )
        return self


class GetTimeseriesListOutput(BaseModel):
    data: List[Dict[str, str]] = Field(
        ...,
        description="list of available timeseries. The variable ts_id can be used as input for GetTimeseriesValuesInput.",
    )
    description: str = Field(..., description="description of the timeseries data")
