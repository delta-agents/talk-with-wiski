from pydantic import BaseModel, Field, model_validator
from pydantic_ai import ModelRetry
from typing import List, Optional

from talk_with_wiski.models.base import ExampleBaseModel


class GetGroupListInput(ExampleBaseModel):
    """
    Input model for GetGroupList tool.
    """

    number_of_groups_retrieved: int = Field(
        default=5, description="Number of groups to retrieve, default is 5"
    )
    group_name: Optional[str | List[str]] = Field(
        default=None,
        description="Group name or names for which to list all available parameters.",
    )
    group_purpose: Optional[str | List[str]] = Field(
        default=None,
        description="Group purpose or purposes for which to list all available parameters.",
    )
    group_type: Optional[str] = Field(
        default=None,
        description="valid values are 'station', 'parameter', 'timeseries' and 'timeseries_dynamic'",
    )

    @model_validator(mode="after")
    def validate_exclusive_fields(cls, values):
        group_name, group_purpose, group_type = (
            values.group_name,
            values.group_purpose,
            values.group_type,
        )
        if group_name and group_purpose:
            raise ModelRetry(
                "Only one of 'group_name' or 'group_purpose' can be provided, not both."
            )
        if group_type is not None:
            if group_type not in [
                "station",
                "parameter",
                "timeseries",
                "timeseries_dynamic",
            ]:
                raise ModelRetry(
                    "Invalid value for 'group_type'. Must be one of: "
                    "'station', 'parameter', 'timeseries', 'timeseries_dynamic'."
                )
        return values


class GroupItem(BaseModel):
    group_name: str
    group_type: str
    group_id: int
    group_remark: str
    group_purpose: str
    group_private: bool


class GetGroupListOutput(BaseModel):
    group_item_list: List[GroupItem] = Field(
        ..., description="list of GroupItem objects"
    )
    description: str = Field(..., description="Grouplists")
