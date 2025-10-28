from fastapi import APIRouter
from fastmcp import FastMCP
from talk_with_wiski.utils.docstring_generator import auto_docstring
from talk_with_wiski.models import (
    AddIndexInput,
    AddIndexOutput,
)
from talk_with_wiski.tools import add_index as add_index_pydanctic_ai

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
@router.post("/tools.agent1/add_index")
@auto_docstring(
    "Tool to add index. Can also be used to subtract if negative numbers are provided."
)
async def add_index(
    input: AddIndexInput,
) -> AddIndexOutput:
    ctx = get_runtime_ctx()
    return await add_index_pydanctic_ai(ctx, input)
