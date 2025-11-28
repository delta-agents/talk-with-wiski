from pydantic import Field, model_validator
from pydantic_ai import ModelRetry
from typing import Dict, List, Optional

from talk_with_wiski.models.base import WiskiBaseModel


class GetTimeseriesListInput(WiskiBaseModel):
    """
    Input model for get_timeseries_list tool.
    Currently, no parameters are required, but this can be extended in the future.
    """

    station_no: Optional[str | List[str]] = Field(
        default=None,
        description="Station number or numbers for which to list all available parameters."
        "List of 1 or more, * as wildcard is allowed."
        "This variable can be obtained from GetLocationsOutput (the output of the function get_locations)",
    )
    station_name: Optional[str | List[str]] = Field(
        default=None,
        description="Station name or names for which to list all available parameters."
        "List of 1 or more, * as wildcard is allowed."
        "This variable can be obtained from GetLocationsOutput (the output of the function get_locations)",
    )
    # site_no: Optional[str | List[str]] = Field(
    #     default=None,
    #     description="Site number or numbers for which to list all available parameters."
    #     "This variable can be obtained from GetSitesOutput (the output of the function get_sites)",
    # )
    parametertype_name: Optional[str | List[str]] = Field(
        default=None,
        description="List all available parameters that feature the parameter type. "
        "This variable can be obtained from GetParametersOutput or GetParametertypeListOutput (the output of the function get_parameters or get_parametertype_list)"
        "List of 1 or more, * as wildcard is allowed, "
        "examples of parametertype_names are 'WNS*' or 'Evaporation'"
        "WNS staat voor Waarnemingssoort volgens de Aquo-standaard van Informatiehuis Water"
        "zie https://www.aquo.nl/index.php/Id-a225c399-903d-4ee1-ec2f-521b4f255cb5",
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


class GetTimeseriesListOutput(WiskiBaseModel):
    data: List[Dict[str, str]] = Field(
        ...,
        description="list of available timeseries. The variable ts_id can be used as input for GetTimeseriesValuesInput.",
    )
    description: str = Field(..., description="description of the timeseries data")
