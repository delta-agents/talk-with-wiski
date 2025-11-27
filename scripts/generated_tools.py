"""
Auto-generated pydantic-ai Tool definitions from FastMCP OpenAPI spec.
"""

from pydantic_ai import Tool

# Import tool functions
from talk_with_wiski.tools import (
    analyse_timeseries_availability,
    analyse_timeseries_quality_code,
    analyse_timeseries_statistics,
    analyse_timeseries_thresholds,
    analyse_timeseries_trend,
    get_group_list,
    get_locations,
    get_metadata,
    get_parameters,
    get_parametertype_list,
    get_sites,
    get_timeseries_list,
    get_timeseries_type,
    get_timeseries_values,
)


# Tool definitions with descriptions from FastMCP
tools = [
    Tool(
        get_locations,
        takes_ctx=True,
        name="get_locations",
        description="Retrieves get locations from the WISKI API\n\nParameters:\n- requested_geolocation (array): Requested geolocation for geocoding to a certain location in lon/lat, stations are searched within radius of geoloc (e.g. [Breda, 5.0])\n- station_no (array): Name of station (station_no). Total to return smaller than 5\n- station_id (array): Index to use (station_id) in the example tool. Total to return smaller than 5\n- max_number_of_station_ids (integer): Maximum number is by default 5. If more required, increase this number\n- returnfields (string): Returnfields from API as string\n- bbox (array): bbox to clip data",
    ),
    Tool(
        get_parameters,
        takes_ctx=True,
        name="get_parameters",
        description="Retrieves get parameters from the WISKI API\n\nParameters:\n- station_no (string | array): Station number or numbers for which to list all available parameters.\n- site_no (string | array): Site number or numbersfor which to list all available parameters.\n- parameter_type (string): List all available parameters that feature the parameter type. Examples of parameter types are 'debiet', 'waterhoogte' or 'drempelhoogte'",
    ),
    Tool(
        get_sites,
        takes_ctx=True,
        name="get_sites",
        description="Retrieves get sites from the WISKI API\n\nParameters:\n- site_no (array): Name of station (station_no). Total to return smaller than 5\n- site_id (array): Index to use (station_id) in the example tool. Total to return smaller than 5\n- max_number_of_site_ids (integer): Index to use (station_id) in the example tool. Total to return smaller than 5\n- returnfields (string): Returnfields from API as string",
    ),
    Tool(
        get_group_list,
        takes_ctx=True,
        name="get_group_list",
        description="Retrieves get group list from the WISKI API\n\nParameters:\n- number_of_groups_retrieved (integer): Number of groups to retrieve, default is 5\n- group_name (string | array): Group name or names for which to list all available parameters.\n- group_purpose (string | array): Group purpose or purposes for which to list all available parameters.\n- group_type (string): valid values are 'station', 'parameter', 'timeseries' and 'timeseries_dynamic'",
    ),
    Tool(
        get_parametertype_list,
        takes_ctx=True,
        name="get_parametertype_list",
        description="Retrieves get parametertype list from the WISKI API\n\nParameters:\n- parametertype_id (array): List of parametertype_id requested. List of 1 or more id, should be integer\n- parametertype_name (array): List of parametertype_name requested. List of 1 or more, wildcards allowed, examples of parametertype_names are 'WNS*' or 'Evaporation'WNS staat voor Waarnemingssoort volgens de Aquo-standaard van Informatiehuis Waterzie https://www.aquo.nl/index.php/Id-a225c399-903d-4ee1-ec2f-521b4f255cb5",
    ),
    Tool(
        get_metadata,
        takes_ctx=True,
        name="get_metadata",
        description="Retrieves get metadata from the WISKI API\n\nParameters:\n- ts_id (string | array): ts_id or list of ts_ids\n- site_no (string | array): site_no or list of site_nos\n- station_no (string | array): station_no or list of station_nos",
    ),
    Tool(
        get_timeseries_list,
        takes_ctx=True,
        name="get_timeseries_list",
        description="Retrieves get timeseries list from the WISKI API\n\nParameters:\n- station_no (string | array): Station number or numbers for which to list all available parameters. This variable can be obtained from GetLocationsOutput (the output of the function get_locations)\n- station_name (string | array): Station name or names for which to list all available parameters. This variable can be obtained from GetLocationsOutput (the output of the function get_locations)\n- site_no (string | array): Site number or numbers for which to list all available parameters. This variable can be obtained from GetSitesOutput (the output of the function get_sites)\n- parametertype_name (string | array): List all available parameters that feature the parameter type. This variable can be obtained from GetParametersOutput or GetParametertypeListOutput (the output of the function get_parameters or get_parametertype_list)",
    ),
    Tool(
        get_timeseries_type,
        takes_ctx=True,
        name="get_timeseries_type",
        description="Retrieves get timeseries type from the WISKI API\n\nParameters:\n- number_of_timeseries_types (integer): Number of timeseries types to retrieve\n- ts_type_id (integer): Timeseries type ID, retrieved from the tool `get_timeseries_list`\n- ts_shortname (string | array): Timeseries short name or names for which to list which type a timeseries is.\n- ts_name (string | array): Timeseries name or names for which to list which type a timeseries is.",
    ),
    Tool(
        get_timeseries_values,
        takes_ctx=True,
        name="get_timeseries_values",
        description="Retrieves get timeseries values from the WISKI API\n\nParameters:\n- ts_id (string | array): Timeseries ID or IDs for which to provide all timeseries data. This variable can be obtained from getTimeseriesListOutput (the output of the function get_timeseries_list)\n- max_number_of_tsids_to_retrieve (integer): Maximum number of timeseries_id to retrieve, default=5, increase this parameterif you need data for more timeseries_ids\n- max_number_of_values_per_tsid (integer): Maximum number of values per timeseries_id to retrieve, default=10, increase this parameterif you need data for more values per timeseries_ids\n- from_date (string): Start date for the timeseries data request. Format must be yyyy-MM-dd or yyyy-MM-dd'T'HH:mm:ss'Z'\n- to_date (string): End date for the timeseries data request. Format must be yyyy-MM-dd or yyyy-MM-dd'T'HH:mm:ss'Z'\n- period (string): Time period for historical timeseries data request. Must be according to ISO format P#Y#M#DT#H#M#S where P just indicates an arbitrary period with the # being integers. 'period=complete' will return the complete coverage of all requested timeseries\n- futureperiod (string): Future time period for future timeseries data request. Must be according to ISO format P#Y#M#DT#H#M#S where P just indicates an arbitrary period with the # being integers\n- returnfields (string): Comma-separated list of fields (spaces allowed) to include in the response. If not specified, all default fields will be included.\n- get_as_url (boolean): Option to get url instead of data in case of large data requests",
    ),
    Tool(
        analyse_timeseries_statistics,
        takes_ctx=True,
        name="analyse_timeseries_statistics",
        description="Re-use Timeseries class from get_timeseries_values.\n\nParameters:\n- ts_id (string): SINGLE ts_id as string for timeseries analysis\n- max_number_of_tsids_to_retrieve (integer): Maximum number of timeseries_id to retrieve, default=5, increase this parameterif you need data for more timeseries_ids\n- max_number_of_values_per_tsid (integer): Maximum number of values per timeseries_id to retrieve, default=10, increase this parameterif you need data for more values per timeseries_ids\n- from_date (string): Start date for the timeseries data request. Format must be yyyy-MM-dd or yyyy-MM-dd'T'HH:mm:ss'Z'\n- to_date (string): End date for the timeseries data request. Format must be yyyy-MM-dd or yyyy-MM-dd'T'HH:mm:ss'Z'\n- period (string): Time period for historical timeseries data request. Must be according to ISO format P#Y#M#DT#H#M#S where P just indicates an arbitrary period with the # being integers. 'period=complete' will return the complete coverage of all requested timeseries\n- futureperiod (string): Future time period for future timeseries data request. Must be according to ISO format P#Y#M#DT#H#M#S where P just indicates an arbitrary period with the # being integers\n- returnfields (string): Comma-separated list of fields (spaces allowed) to include in the response. If not specified, all default fields will be included.\n- get_as_url (boolean): Option to get url instead of data in case of large data requests",
    ),
    Tool(
        analyse_timeseries_thresholds,
        takes_ctx=True,
        name="analyse_timeseries_thresholds",
        description="Re-use Timeseries class from get_timeseries_values.\n\nParameters:\n- ts_id (string): SINGLE ts_id as string for timeseries analysis\n- max_number_of_tsids_to_retrieve (integer): Maximum number of timeseries_id to retrieve, default=5, increase this parameterif you need data for more timeseries_ids\n- max_number_of_values_per_tsid (integer): Maximum number of values per timeseries_id to retrieve, default=10, increase this parameterif you need data for more values per timeseries_ids\n- from_date (string): Start date for the timeseries data request. Format must be yyyy-MM-dd or yyyy-MM-dd'T'HH:mm:ss'Z'\n- to_date (string): End date for the timeseries data request. Format must be yyyy-MM-dd or yyyy-MM-dd'T'HH:mm:ss'Z'\n- period (string): Time period for historical timeseries data request. Must be according to ISO format P#Y#M#DT#H#M#S where P just indicates an arbitrary period with the # being integers. 'period=complete' will return the complete coverage of all requested timeseries\n- futureperiod (string): Future time period for future timeseries data request. Must be according to ISO format P#Y#M#DT#H#M#S where P just indicates an arbitrary period with the # being integers\n- returnfields (string): Comma-separated list of fields (spaces allowed) to include in the response. If not specified, all default fields will be included.\n- get_as_url (boolean): Option to get url instead of data in case of large data requests\n- threshold (number): Threshold value for timeseries analysis",
    ),
    Tool(
        analyse_timeseries_trend,
        takes_ctx=True,
        name="analyse_timeseries_trend",
        description="Re-use Timeseries class from get_timeseries_values.\n\nParameters:\n- ts_id (string): SINGLE ts_id as string for timeseries analysis\n- max_number_of_tsids_to_retrieve (integer): Maximum number of timeseries_id to retrieve, default=5, increase this parameterif you need data for more timeseries_ids\n- max_number_of_values_per_tsid (integer): Maximum number of values per timeseries_id to retrieve, default=10, increase this parameterif you need data for more values per timeseries_ids\n- from_date (string): Start date for the timeseries data request. Format must be yyyy-MM-dd or yyyy-MM-dd'T'HH:mm:ss'Z'\n- to_date (string): End date for the timeseries data request. Format must be yyyy-MM-dd or yyyy-MM-dd'T'HH:mm:ss'Z'\n- period (string): Time period for historical timeseries data request. Must be according to ISO format P#Y#M#DT#H#M#S where P just indicates an arbitrary period with the # being integers. 'period=complete' will return the complete coverage of all requested timeseries\n- futureperiod (string): Future time period for future timeseries data request. Must be according to ISO format P#Y#M#DT#H#M#S where P just indicates an arbitrary period with the # being integers\n- returnfields (string): Comma-separated list of fields (spaces allowed) to include in the response. If not specified, all default fields will be included.\n- get_as_url (boolean): Option to get url instead of data in case of large data requests",
    ),
    Tool(
        analyse_timeseries_availability,
        takes_ctx=True,
        name="analyse_timeseries_availability",
        description="Re-use Timeseries class from get_timeseries_values.\n\nParameters:\n- ts_id (string): SINGLE ts_id as string for timeseries analysis\n- max_number_of_tsids_to_retrieve (integer): Maximum number of timeseries_id to retrieve, default=5, increase this parameterif you need data for more timeseries_ids\n- max_number_of_values_per_tsid (integer): Maximum number of values per timeseries_id to retrieve, default=10, increase this parameterif you need data for more values per timeseries_ids\n- from_date (string): Start date for the timeseries data request. Format must be yyyy-MM-dd or yyyy-MM-dd'T'HH:mm:ss'Z'\n- to_date (string): End date for the timeseries data request. Format must be yyyy-MM-dd or yyyy-MM-dd'T'HH:mm:ss'Z'\n- period (string): Time period for historical timeseries data request. Must be according to ISO format P#Y#M#DT#H#M#S where P just indicates an arbitrary period with the # being integers. 'period=complete' will return the complete coverage of all requested timeseries\n- futureperiod (string): Future time period for future timeseries data request. Must be according to ISO format P#Y#M#DT#H#M#S where P just indicates an arbitrary period with the # being integers\n- returnfields (string): Comma-separated list of fields (spaces allowed) to include in the response. If not specified, all default fields will be included.\n- get_as_url (boolean): Option to get url instead of data in case of large data requests",
    ),
    Tool(
        analyse_timeseries_quality_code,
        takes_ctx=True,
        name="analyse_timeseries_quality_code",
        description="Re-use Timeseries class from get_timeseries_values.\n\nParameters:\n- ts_id (string | array): Timeseries ID or IDs for which to provide all timeseries data. This variable can be obtained from getTimeseriesListOutput (the output of the function get_timeseries_list)\n- max_number_of_tsids_to_retrieve (integer): Maximum number of timeseries_id to retrieve, default=5, increase this parameterif you need data for more timeseries_ids\n- max_number_of_values_per_tsid (integer): Maximum number of values per timeseries_id to retrieve, default=10, increase this parameterif you need data for more values per timeseries_ids\n- from_date (string): Start date for the timeseries data request. Format must be yyyy-MM-dd or yyyy-MM-dd'T'HH:mm:ss'Z'\n- to_date (string): End date for the timeseries data request. Format must be yyyy-MM-dd or yyyy-MM-dd'T'HH:mm:ss'Z'\n- period (string): Time period for historical timeseries data request. Must be according to ISO format P#Y#M#DT#H#M#S where P just indicates an arbitrary period with the # being integers. 'period=complete' will return the complete coverage of all requested timeseries\n- futureperiod (string): Future time period for future timeseries data request. Must be according to ISO format P#Y#M#DT#H#M#S where P just indicates an arbitrary period with the # being integers\n- returnfields (string): Comma-separated list of fields (spaces allowed) to include in the response. If not specified, all default fields will be included.\n- get_as_url (boolean): Option to get url instead of data in case of large data requests",
    ),
]
