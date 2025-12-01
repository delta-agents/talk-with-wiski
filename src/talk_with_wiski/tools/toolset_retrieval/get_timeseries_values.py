import requests
import json

from talk_with_wiski.models.modelset_retrieval.get_timeseries_values import (
    GetTimeseriesValuesInput,
    GetTimeseriesValuesOutput,
    Timeseries,
)
from talk_with_wiski.utils.logging_utils import log_tool_call, logger


@log_tool_call
async def get_timeseries_values(
    ctx, input: GetTimeseriesValuesInput
) -> GetTimeseriesValuesOutput:
    """
    Show the timeseries data
    """

    #  you can access any context added to the ctx: Deps object
    url = ctx.deps.url

    # base url
    endpoint = url + "KiWIS"
    params = {
        "datasource": "0",
        "service": "kisters",
        "type": "queryServices",
        "request": "getTimeseriesValues",
        "format": "dajson",
        "metadata": "true",
    }

    data = _get_timeseries_request(endpoint, input, params)

    # return GetTimeseriesValuesOutput(data=data, description="Timeseries")

    # max aantal elementen dat default mag worden teruggegeven
    n_ids = input.max_number_of_tsids_to_retrieve
    n_vals = input.max_number_of_values_per_tsid

    # used for debugging
    logger.debug(f"number of tsids to retrieve: {n_ids}")
    logger.debug(f"number of values per tsid to retrieve: {n_vals}")

    logger.debug(data)
    # data vullen
    timeseries_values_list = []
    for timeseries_values in data:
        timeseries_values["ts_id"] = int(timeseries_values["ts_id"])
        # limit number of data points
        timeseries_values["data"] = timeseries_values["data"][:n_vals]
        # Append as Timeseries object
        timeseries_values_list.append(Timeseries(**timeseries_values))

    timeseries_values_list = timeseries_values_list[:n_ids]
    description = (
        f"Timeseries values retrieved successfully, containing a total of {len(timeseries_values_list)} ts_ids,"
        f"with max {str(n_vals)} data values per ts_id (increase "
        "number_of_timeseries_values_per_id"
        " if more data required)."
    )
    if len(timeseries_values_list) > n_ids:
        description += f"Only the first {n_ids} items are returned, search for specific items using the provided filters or increase the number of items requested."

    if input.get_as_url:
        # get url without actually doing a request
        req = requests.Request("GET", endpoint, params=params)
        prepared = req.prepare()
        # only return URL
        return GetTimeseriesValuesOutput(
            timeseries_values_list=timeseries_values_list,
            description="Reduced data in timeseries_values_list, use provided URL to retrieve full dataset",
            url=prepared.url,
        )

    else:
        return GetTimeseriesValuesOutput(
            timeseries_values_list=timeseries_values_list,
            description=description,
            url="",
        )


# Function to retrieve data from WISKI
def _get_timeseries_request(endpoint, input, params):
    # extend url
    if isinstance(input.ts_id, list):
        params["ts_id"] = ",".join(input.ts_id)
    else:
        params["ts_id"] = input.ts_id

    if input.from_date is not None:
        params["from"] = input.from_date

    if input.to_date is not None:
        params["to"] = input.to_date

    if input.period is not None:
        params["period"] = input.period

    if input.futureperiod is not None:
        params["futureperiod"] = input.futureperiod

    if input.returnfields is not None:
        params["returnfields"] = input.returnfields

    if input.include_quality_codes:
        params["returnfields"] = "Timestamp,Value,Quality Code"

    # for debugging
    # req = requests.Request("GET", endpoint, params=params)
    # prepared = req.prepare()
    # print(prepared.url)

    # Data ophalen
    res = requests.get(endpoint, params=params, timeout=30)
    data = list(json.loads(res.text))

    return data
