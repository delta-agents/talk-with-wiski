"""
WISKI Agent.

This module defines the agent that can answer questions about WISKI .
"""

import os
from pydantic_ai import Agent, Tool
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.agent import AgentRunResult

from talk_with_wiski.models.base import Deps, AgentResponse

# Import logging utilities from the dedicated module
from talk_with_wiski.utils.logging_utils import logger, setup_logging

# Import the tool functions directly
from talk_with_wiski.tools import (
    get_locations,
    get_parameters,
    get_group_list,
    get_sites,
    get_timeseries_list,
    get_timeseries_values,
    get_timeseries_type,
    get_parametertype_list,
    get_metadata,
    analyse_timeseries_statistics,
    analyse_timeseries_thresholds,
    analyse_timeseries_trend,
    analyse_timeseries_quality_code,
    analyse_timeseries_availability,
)


class WISKIAgent:
    """
    Agent for querying and analyzing WISKI .

    Initialize the WISKI Agent.

    Args:
        db_path: Path to the SQLite database containing WISKI data
        model: Optional model to use (defaults to PRIMARY_MODEL env var or gpt-4)
        api_key: Optional API key (will use OPENROUTER_API_KEY env var if not provided)
        base_url: Optional base URL (will use OPENROUTER_BASE_URL env var if not provided)
        log_level: Logging level (default is INFO)
        log_dir: Directory where log files will be stored (default is ~/.WISKI_agent/logs)
    """

    def __init__(
        self,
        model: str = None,
        api_key: str = None,
        base_url: str = None,
        log_level: str = "INFO",
        log_dir: str = None,
    ):
        # Read model name from PRIMARY_MODEL env var if available
        primary_model = os.environ.get("PRIMARY_MODEL")
        default_model = "gpt-4"

        if primary_model:
            logger.info(f"Using model from PRIMARY_MODEL env: {primary_model}")
            default_model = primary_model

        self.model_name = model or default_model
        self.api_key = api_key
        self.base_url = base_url
        self.agent = None
        self.db_connection = None
        self.url = os.environ.get("WISKI_URL")

        # Set up logging
        setup_logging(log_level=log_level, log_dir=log_dir)

        logger.info(f"Using model: {self.model_name}")
        if log_dir:
            logger.info(f"Logging to directory: {log_dir}")

    def _create_agent(self):
        """Create the Talk with WISKI Agent with connection to the Fast MCP instance."""
        if self.agent is not None:
            return

        # Create a simplified system prompt with the schema information
        system_prompt = (
            "You are the Talk with WISKI Agent for analyzing a Water Information System API. "
            "Your capabilities include retrieving and analyzing location, parameters, timeseriessets. "
            "You can visualize data flows only using mermaid diagram syntax.\n\n"
            "Response Format:\n"
            "- You response shall be in Dutch\n"
            "- Use available tools to gather accurate information first\n"
            "- Include explanatory text in markdown format\n"
            "- Add tables when appropriate (markdown format)\n"
            "- Include mermaid diagrams when visualizing relationships\n\n"
            "Always structure your response with text first, followed by tables and diagrams if needed."
        )

        # Create the model with OpenRouter
        api_key = self.api_key or os.environ.get("OPENROUTER_API_KEY")
        base_url = self.base_url or os.environ.get("OPENROUTER_BASE_URL")

        if not api_key:
            raise ValueError(
                "API key not provided. Either pass as api_key parameter or set OPENROUTER_API_KEY environment variable."
            )
        # Updated syntax for newer pydantic-ai versions

        model = OpenAIChatModel(
            model_name=self.model_name,
            provider=OpenAIProvider(base_url=base_url, api_key=api_key),
        )

        # Create the agent
        logger.info(f"Creating WISKI Agent using {self.model_name}")
        if base_url:
            logger.info(f"Using custom base URL: {base_url}")

        # Dit is een manier om de tools toe te voegen aan de agent
        # scripts/mcp_to_agent.py genereert deze code automatisch in scripts/generated_tools.py
        self.agent = Agent(
            model=model,
            system_prompt=system_prompt,
            deps_type=Deps,
            output_type=AgentResponse,
            tools=[
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
            ],
        )
        # Andere mogelijkheid, maar dan moet de mcp server draaien
        # from pydantic_ai.toolsets.fastmcp import FastMCPToolset
        # toolset = FastMCPToolset('http://localhost:8000/mcp')
        # self.agent = Agent(
        #     model=model,
        #     system_prompt=system_prompt,
        #     output_type=AgentResponse,
        #     tools=[toolset]
        # )
        # Initialize deps with database path
        self.deps = Deps(url=self.url)

        return self

    async def ask(self, question: str) -> "AgentRunResult":
        """
        Ask the WISKI Agent a question.

        Args:
            question: The question to ask

        Returns:
            AgentRunResult: The agent's response object containing AgentResponse in its data property
        """
        if self.agent is None:
            self._create_agent()

        logger.info(f"Asking agent: {question}")

        try:
            # Use basic run method
            response = await self.agent.run(question, deps=self.deps)
            return response

        except Exception as e:
            logger.error(f"Error asking agent: {str(e)}")
            raise
