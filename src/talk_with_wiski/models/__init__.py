# Config
from talk_with_wiski.models.modelset_1.example1 import (
    AddIndexInput,
    AddIndexOutput,
)

from talk_with_wiski.models.modelset_2.example2 import (
    Example2Input,
    Example2Output,
)

from talk_with_wiski.models.modelset_retrieval.get_locations import (
    GetLocationsInput,
    GetLocationsOutput,
)

from talk_with_wiski.models.modelset_retrieval.get_sites import (
    GetSitesInput,
    GetSitesOutput,
)

from talk_with_wiski.models.modelset_retrieval.get_parameters import (
    GetParametersInput,
    GetParametersOutput,
)

from talk_with_wiski.models.modelset_retrieval.get_group_list import (
    GetGroupListInput,
    GetGroupListOutput,
    GroupItem,
)

__all__ = [
    "AddIndexInput",
    "AddIndexOutput",
    "Example2Input",
    "Example2Output",
    "GetLocationsInput",
    "GetLocationsOutput",
    "GetSitesInput",
    "GetSitesOutput",
    "GetParametersInput",
    "GetParametersOutput",
    "GetGroupListInput",
    "GetGroupListOutput",
    "GroupItem",
]
