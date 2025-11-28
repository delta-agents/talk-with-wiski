from pydantic import Field, model_validator
from pydantic_ai import ModelRetry
from typing import Dict, List, Optional

from talk_with_wiski.models.base import WiskiBaseModel


class GetParametertypeListInput(WiskiBaseModel):
    """
    Input model for get_parameter_type_list tool.
    """

    parametertype_id: Optional[List[int]] = Field(
        default=None,
        description="List of parametertype_id requested. List of 1 or more id, should be integer",
    )
    parametertype_name: Optional[List[str]] = Field(
        default=None,
        description="List of parametertype_name requested. List of 1 or more, * as wildcard is allowed, "
        "examples of parametertype_names are 'WNS*' or 'Evaporation'"
        "WNS staat voor Waarnemingssoort volgens de Aquo-standaard van Informatiehuis Water"
        "zie https://www.aquo.nl/index.php/Id-a225c399-903d-4ee1-ec2f-521b4f255cb5",
    )

    @model_validator(mode="after")
    def validate_exclusive_fields(self):
        parametertype_id, parametertype_name = (
            self.parametertype_id,
            self.parametertype_name,
        )
        if parametertype_id and parametertype_name:
            raise ModelRetry(
                "Only one of 'parametertype_id' or 'parametertype_name' can be provided, not both."
            )
        if parametertype_id is not None and "*" in parametertype_id:
            raise ModelRetry(
                "Wildcard (*) is only allowed for parametertype_name, e.g. WNS*."
            )
        return self


class GetParametertypeListOutput(WiskiBaseModel):
    """
    Output model for get_parameter_type_list tool.
    """

    data: List[Dict[str, str]] = Field(
        ...,
        description="List containing dictionaries with pairs of parametertype_id and parametertype_name",
    )
    description: str = Field(..., description="Parameters")
