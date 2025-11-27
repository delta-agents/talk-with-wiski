"""
FEWS Webservice Agent.

This module defines the agent that can answer questions about FEWS webservice.
"""

import os
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.agent import AgentRunResult

from talk_with_wiski.models.base import Deps, AgentResponse

# Import logging utilities from the dedicated module
from talk_with_wiski.utils.logging_utils import logger, setup_logging

# Import the mcp instance with all registered tools
from talk_with_wiski.routers.tools_router_Wiski import mcp


class FEWSWebserviceAgent:
    """
    Agent for querying and analyzing FEWS Webservice.

    Initialize the FEWS Webservice Agent.

    Args:
        db_path: Path to the SQLite database containing FEWS webservice data
        model: Optional model to use (defaults to PRIMARY_MODEL env var or gpt-4)
        api_key: Optional API key (will use OPENROUTER_API_KEY env var if not provided)
        base_url: Optional base URL (will use OPENROUTER_BASE_URL env var if not provided)
        log_level: Logging level (default is INFO)
        log_dir: Directory where log files will be stored (default is ~/.fews_agent/logs)
    """

    def __init__(
        self,
        db_path: str,
        model: str = None,
        api_key: str = None,
        base_url: str = None,
        log_level: str = "INFO",
        log_dir: str = None,
    ):
        self.db_path = db_path

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

        # Set up logging
        setup_logging(log_level=log_level, log_dir=log_dir)

        logger.info(f"Initialized FEWSWebserviceAgent with database: {db_path}")
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

        # Create the model with OpenRouter Webservice
        api_key = self.api_key or os.environ.get("OPENROUTER_API_KEY")
        base_url = self.base_url or os.environ.get("OPENROUTER_BASE_URL")

        if not api_key:
            raise ValueError(
                "API key not provided. Either pass as api_key parameter or set OPENROUTER_API_KEY environment variable."
            )
        # Updated syntax for newer pydantic-ai versions

        model = OpenAIChatModel(
            self.model_name,
            base_url=base_url,
            api_key=api_key,
        )

        # Create the agent
        logger.info(f"Creating FEWS Webservice Agent using {self.model_name}")
        if base_url:
            logger.info(f"Using custom base URL: {base_url}")

        # Create agent with MCP tools from the router
        self.agent = Agent(
            model=model,
            toolsets=[mcp],
            system_prompt=system_prompt,
            deps_type=Deps,
            output_type=AgentResponse,
        )

        # Initialize deps with database path
        self.deps = Deps(url=self.db_path)

        return self

    async def ask(self, question: str) -> "AgentRunResult":
        """
        Ask the FEWS Webservice Agent a question.

        Args:
            question: The question to ask

        Returns:
            AgentRunResult: The agent's response object containing AgentResponse in its data property
        """
        if self.agent is None:
            self.connect()

        logger.info(f"Asking agent: {question}")

        try:
            # Use basic run method
            response = await self.agent.run(question, deps=self.deps)
            return response

        except Exception as e:
            logger.error(f"Error asking agent: {str(e)}")
            raise
