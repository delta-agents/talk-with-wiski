from pydantic import Field, model_validator
from pydantic_ai import ModelRetry
from typing import Dict, List, Optional

from talk_with_wiski.models.base import WiskiBaseModel


class GetParametersInput(WiskiBaseModel):
    """
    Input model for get_parameters tool.
    """

    station_no: Optional[str | List[str]] = Field(
        default=None,
        description="Station number or numbers for which to list all available parameters.",
    )
    site_no: Optional[str | List[str]] = Field(
        default=None,
        description="Site number or numbersfor which to list all available parameters.",
    )
    parametertype_name: Optional[str | List[str]] = Field(
        default=None,
        description="List of parametertype_name requested. List of 1 or more, * as wildcard is allowed, "
        "examples of parametertype_names are 'WNS*' or 'Evaporation'"
        "WNS staat voor Waarnemingssoort volgens de Aquo-standaard van Informatiehuis Water"
        "zie https://www.aquo.nl/index.php/Id-a225c399-903d-4ee1-ec2f-521b4f255cb5",
    )
    parameter_type: Optional[str] = Field(
        default=None,
        description="Filter the output to list all available parameters that feature the parameter type. Examples of parameter types are 'debiet', 'waterhoogte' or 'drempelhoogte'",
    )

    @model_validator(mode="after")
    def validate_exclusive_fields(self):
        station_no, site_no, parametertype_name, parameter_type = (
            self.station_no,
            self.site_no,
            self.parametertype_name,
            self.parameter_type,
        )
        if station_no and site_no:
            raise ModelRetry(
                "Only one of 'station_no' or 'site_no' can be provided, not both."
            )
        if parametertype_name and site_no:
            raise ModelRetry(
                "Only one of 'parametertype_name' or 'parameter_type' can be provided, not both."
            )
        return self


class GetParametersOutput(WiskiBaseModel):
    """
    Output model for get_parameters tool.
    """

    data: List[Dict[str, str]] = Field(..., description="list of parameter dictionary")
    description: str = Field(..., description="Parameters")
