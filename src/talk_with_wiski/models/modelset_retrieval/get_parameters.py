from pydantic import BaseModel, Field, model_validator
from pydantic_ai import ModelRetry
from typing import Dict, List, Optional

from talk_with_wiski.models.base import ExampleBaseModel


class GetParametersInput(ExampleBaseModel):
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
    parameter_type: Optional[str] = Field(
        default=None,
        description="List all available parameters that feature the parameter type. Examples of parameter types are 'debiet', 'waterhoogte' or 'drempelhoogte'",
    )

    @model_validator(mode="after")
    def validate_exclusive_fields(cls, values):
        station_no, site_no = (
            values.station_no,
            values.site_no,
        )
        if station_no and site_no:
            raise ModelRetry(
                "Only one of 'station_no' or 'site_no' can be provided, not both."
            )
        return values


class GetParametersOutput(BaseModel):
    """
    Output model for get_parameters tool.
    """

    data: List[Dict[str, str]] = Field(..., description="list of parameter dictionary")
    description: str = Field(..., description="Parameters")
