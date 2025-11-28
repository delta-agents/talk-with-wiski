"""
Script to scrape FastMCP OpenAPI docs and generate pydantic-ai Tool definitions.

Usage:
    1. Start the FastMCP server: uvicorn src.main:app --reload
    2. Run this script: python scripts/mcp_to_agent.py
"""

import requests


def fetch_openapi_spec(base_url: str = "http://localhost:8000") -> dict:
    """Fetch the OpenAPI specification from the FastMCP server."""
    response = requests.get(f"{base_url}/openapi.json")
    response.raise_for_status()
    return response.json()


def extract_tool_info(openapi_spec: dict) -> list[dict]:
    """Extract tool information from OpenAPI spec, including parameter descriptions."""
    tools = []
    paths = openapi_spec.get("paths", {})
    schemas = openapi_spec.get("components", {}).get("schemas", {})

    for path, methods in paths.items():
        # Only process /tools/* endpoints
        if not path.startswith("/tools/"):
            continue

        for method, details in methods.items():
            if method != "post":
                continue

            # Extract tool name from path (e.g., /tools/get_parameters -> get_parameters)
            tool_name = path.replace("/tools/", "")

            # Get request body schema reference
            request_body = details.get("requestBody", {})
            content = request_body.get("content", {})
            json_content = content.get("application/json", {})
            schema_ref = json_content.get("schema", {}).get("$ref", "")

            # Extract input model name from schema reference
            input_model = ""
            if schema_ref:
                input_model = schema_ref.split("/")[-1]

            # Build rich description from input model schema
            description = build_tool_description(tool_name, input_model, schemas)

            # Get response schema
            responses = details.get("responses", {})
            success_response = responses.get("200", {})
            response_content = success_response.get("content", {}).get(
                "application/json", {}
            )
            response_schema_ref = response_content.get("schema", {}).get("$ref", "")
            output_model = ""
            if response_schema_ref:
                output_model = response_schema_ref.split("/")[-1]

            tools.append(
                {
                    "name": tool_name,
                    "description": description,
                    "input_model": input_model,
                    "output_model": output_model,
                    "path": path,
                }
            )

    return tools


def build_tool_description(tool_name: str, input_model: str, schemas: dict) -> str:
    """Build a rich description from the input model's schema including parameters."""
    # Start with a base description from tool name
    base_desc = tool_name.replace("_", " ").title()

    if not input_model or input_model not in schemas:
        return f"Retrieves {base_desc.lower()} from the WISKI API"

    schema = schemas[input_model]
    model_desc = schema.get("description", "")
    properties = schema.get("properties", {})

    # Build description with parameters
    parts = []

    # Add model description or generate one
    if model_desc and "Input model" not in model_desc:
        parts.append(model_desc)
    else:
        parts.append(f"Retrieves {base_desc.lower()} from the WISKI API")

    # Add parameter descriptions
    if properties:
        parts.append("\n\nParameters:")
        for param_name, param_info in properties.items():
            param_desc = param_info.get("description", "")
            param_type = param_info.get("type", "")

            # Handle anyOf types
            if "anyOf" in param_info:
                types = [
                    t.get("type", "") for t in param_info["anyOf"] if t.get("type")
                ]
                param_type = " | ".join(t for t in types if t != "null")

            if param_desc:
                parts.append(f"\n- {param_name} ({param_type}): {param_desc}")
            else:
                parts.append(f"\n- {param_name} ({param_type})")

    return "".join(parts)


def generate_tool_code(tools: list[dict]) -> str:
    """Generate Python code for pydantic-ai Tool definitions."""

    # Collect unique imports
    input_models = set()
    output_models = set()
    tool_names = set()

    for tool in tools:
        if tool["input_model"]:
            input_models.add(tool["input_model"])
        if tool["output_model"]:
            output_models.add(tool["output_model"])
        tool_names.add(tool["name"])

    # Generate imports
    code_lines = [
        '"""',
        "Auto-generated pydantic-ai Tool definitions from FastMCP OpenAPI spec.",
        '"""',
        "",
        "from pydantic_ai import Tool",
        "",
        "# Import tool functions",
        "from talk_with_wiski.tools import (",
    ]

    for name in sorted(tool_names):
        code_lines.append(f"    {name},")

    code_lines.extend(
        [
            ")",
            "",
            "",
            "# Tool definitions with descriptions from FastMCP",
            "tools = [",
        ]
    )

    # Generate Tool definitions
    for tool in tools:
        description = tool["description"].replace('"', '\\"').replace("\n", "\\n")
        code_lines.append("    Tool(")
        code_lines.append(f"        {tool['name']},")
        code_lines.append("        takes_ctx=True,")
        code_lines.append(f'        name="{tool["name"]}",')
        code_lines.append(f'        description="{description}",')
        code_lines.append("    ),")

    code_lines.extend(
        [
            "]",
            "",
        ]
    )

    return "\n".join(code_lines)


def generate_tool_list_simple(tools: list[dict]) -> str:
    """Generate a simple list format for copy-pasting into Agent definition."""

    code_lines = [
        "# Copy this into your Agent definition:",
        "from pydantic_ai import Tool",
        "",
        "tools = [",
    ]

    for tool in tools:
        desc = tool["description"].replace('"', '\\"').replace("\n", " ")
        # Truncate very long descriptions
        if len(desc) > 200:
            desc = desc[:197] + "..."
        code_lines.append(
            f'    Tool({tool["name"]}, takes_ctx=True, name="{tool["name"]}", description="{desc}"),'
        )

    code_lines.append("]")

    return "\n".join(code_lines)


def print_tool_summary(tools: list[dict]):
    """Print a summary of discovered tools."""
    print(f"\n{'=' * 60}")
    print(f"Found {len(tools)} tools:")
    print(f"{'=' * 60}\n")

    for tool in tools:
        print(f"📦 {tool['name']}")
        print(
            f"   Description: {tool['description'][:80]}..."
            if len(tool["description"]) > 80
            else f"   Description: {tool['description']}"
        )
        print(f"   Input: {tool['input_model']}")
        print(f"   Output: {tool['output_model']}")
        print()


def main():
    """Main function to scrape FastMCP and generate Tool definitions."""
    base_url = "http://localhost:8001"

    print(f"Fetching OpenAPI spec from {base_url}/openapi.json ...")

    try:
        openapi_spec = fetch_openapi_spec(base_url)
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Error: Could not connect to {base_url}")
        print("   Make sure the FastMCP server is running:")
        print("   uvicorn src.main:app --reload")
        return
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return

    # Extract tool info
    tools = extract_tool_info(openapi_spec)

    if not tools:
        print("\n⚠️  No tools found in /tools/* endpoints")
        return

    # Print summary
    print_tool_summary(tools)

    # Generate code
    print(f"{'=' * 60}")
    print("Generated Tool definitions:")
    print(f"{'=' * 60}\n")

    code = generate_tool_list_simple(tools)
    print(code)

    # Save to file
    output_file = "scripts/generated_tools.py"
    full_code = generate_tool_code(tools)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_code)

    print(f"\n✅ Full code saved to: {output_file}")


if __name__ == "__main__":
    main()
