from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.talk_with_wiski.routers.tools_router_Agent1 import (
    router as router_agent1,
)
from src.talk_with_wiski.routers.tools_router_Agent1 import (
    mcp as mcp_agent1,
)
from src.talk_with_wiski.routers.tools_router_Agent2 import (
    router as router_agent2,
)
from src.talk_with_wiski.routers.tools_router_Agent2 import (
    mcp as mcp_agent2,
)
from src.talk_with_wiski.routers.tools_router_Wiski import (
    router as router_wiski,
)
from src.talk_with_wiski.routers.tools_router_Wiski import (
    mcp as mcp_wiski,
)
from typing import AsyncIterator
from dotenv import load_dotenv
from contextlib import asynccontextmanager

load_dotenv(dotenv_path="env/.env")

## Talk With Config

# Mount MCP at /mcp
mcp_app_config = mcp_agent1.http_app(
    path="/", transport="streamable-http", stateless_http=True
)

mcp_app_validator = mcp_agent2.http_app(
    path="/", transport="streamable-http", stateless_http=True
)

mcp_app_wiski = mcp_wiski.http_app(
    path="/", transport="streamable-http", stateless_http=True
)


@asynccontextmanager
async def combined_lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Run both lifespans in startup
    async with (
        mcp_app_config.lifespan(mcp_app_config),
        mcp_app_validator.lifespan(mcp_app_validator),
        mcp_app_wiski.lifespan(mcp_app_wiski),
    ):
        yield


app = FastAPI(
    title="Talk with WISKI Tools API",
    version="0.1.0",
    description="API and MCP server exposing selected tools",
    lifespan=combined_lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the tools router
app.include_router(router_agent1)

# Mount MCP at /mcp
app.mount("/mcp/agent1", mcp_app_config)

# Include the tools router
app.include_router(router_agent2)

# Mount MCP at /mcp
app.mount("/mcp/agent2", mcp_app_validator)

app.include_router(router_wiski)

app.mount("/mcp/wiski", mcp_app_wiski)
