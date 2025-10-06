from fastapi import APIRouter
from fastmcp import FastMCP
from talk_with_wiski.utils.docstring_generator import auto_docstring
from talk_with_wiski.models import (
    Example1Input,
    Example1Output,
)
from talk_with_wiski.tools import example1 as example1_pydanctic_ai

# Import tool functions and their models
from talk_with_wiski.routers.setup_connections import get_runtime_ctx

router = APIRouter()

### in case of authentication
# from talk_with_wiski.routers.setup_connections import setup_env
# from fastmcp.server.auth.providers.jwt import StaticTokenVerifier
# tokens = setup_env()
# verifier = StaticTokenVerifier(tokens=tokens, required_scopes=["read:data"])
# mcp = FastMCP(name="Agent1", verifier=verifier)

mcp = FastMCP(name="Agent1")


# describe_timeseries tool registration
@mcp.tool()
@router.post("/tools.agent1/example1")
@auto_docstring("example1")
async def example1(
    input: Example1Input,
) -> Example1Output:
    ctx = get_runtime_ctx()
    return await example1_pydanctic_ai(ctx, input)
