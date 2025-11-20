"""
Example of a tool cal
"""

from talk_with_wiski.models.modelset_retrieval.get_group_list import (
    GetGroupListInput,
    GetGroupListOutput,
    GroupItem,
)
from talk_with_wiski.utils.logging_utils import log_tool_call
import requests
import json


@log_tool_call
async def get_group_list(ctx, input: GetGroupListInput) -> GetGroupListOutput:
    """
    Show available group lists
    """

    #  you can access any context added to the ctx: Deps object
    url = ctx.deps.url

    # base url
    endpoint = url + "KiWIS"
    params = {
        "datasource": "0",
        "service": "kisters",
        "type": "queryServices",
        "request": "getGroupList",
        "format": "objson",
        "returnfields": "group_name,group_type,group_id,group_remark,group_purpose,group_private,ca_group",
    }

    # extend url
    if input.group_name is not None:
        if isinstance(input.group_name, list):
            params["group_name"] = ",".join(input.group_name)
        else:
            params["group_name"] = input.group_name

    if input.group_purpose is not None:
        if isinstance(input.group_purpose, list):
            params["group_purpose"] = ",".join(input.group_purpose)
        else:
            params["group_purpose"] = input.group_purpose

    # requst data
    res = requests.get(endpoint, params=params, timeout=30)
    data = list(json.loads(res.text))

    group_item_list = []
    for group_item in data:
        group_item["group_id"] = int(group_item["group_id"])
        group_item["group_private"] = bool(group_item["group_private"] == "true")
        group_item_list.append(GroupItem(**group_item))

    n = input.number_of_groups_retrieved
    group_item_list = group_item_list[:n]
    description = f"Group list retrieved successfully, containing a total of  {len(group_item_list)} items."
    description += f"Only the first {n} items are returned, search for specific items using the provided filters or increase the number of items requested."
    return GetGroupListOutput(group_item_list=group_item_list, description=description)
