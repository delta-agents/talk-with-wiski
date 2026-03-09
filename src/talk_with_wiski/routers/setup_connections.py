import json
import os
from pathlib import Path
import warnings
from dotenv import load_dotenv
from requests import Request
from pydantic_ai import RunContext
from fastmcp.server.dependencies import get_http_request
from talk_with_wiski.models.base import Deps
import duckdb


class CtxWithDeps:
    def __init__(self, deps):
        self.deps = deps


# Shared/cached context globals
_cache_database_db = None
_url = None


def setup_env():
    """Load environment variables from a .env file located in the 'env' directory."""
    env_dir = Path(__file__).parent.parent.parent.parent / "env"
    load_dotenv(dotenv_path=env_dir / ".env")
    return json.load(
        open(env_dir / os.getenv("STATIC_TOKENS_FILE", ".static_tokens_example.json"))
    )


def get_user_settings(verifier) -> dict:
    """ "
    Extract user settings from the Authorization header using the provided verifier.
    This allows the user tools to have user specific settings
    """
    # maybe could be improved using `get_access_token` from `fastmcp.server.dependencies`
    try:
        request: Request = get_http_request()
    except RuntimeError as e:
        # allow debugging and testing without an HTTP request context
        warnings.warn(
            f"Failed to get HTTP request context {e}, reverting to environment variables."
        )
    else:
        authorization = request.headers.get("Authorization", None)
        if authorization is not None and authorization.startswith("Bearer "):
            authorization = authorization[len("Bearer ") :]
            user_settings = verifier.tokens[authorization]
        else:
            raise ValueError("Missing or invalid Authorization header")

    # Validate WISKI_URL before returning
    wiski_url = user_settings.get("WISKI_URL")
    if not wiski_url:
        raise ValueError(
            "WISKI_URL not configured in user settings. "
            "Please check your authentication token configuration."
        )
    return user_settings

def get_runtime_ctx(user_settings) -> RunContext:
    """
    Returns a RunContext[Deps] with a shared database connection and schema.
    Uses DB_PATH env var or defaults to './database.db'.
    """

    # See talk-with-fews for user based connections: currently only one config
    global _cache_database_db, _url

    # handle webservice URL
    disable_cache_db = os.environ.get("DISABLE_CACHE", False)

    # TODO: later nog toevoegen aan de environmental variables?
    if _url is None:
        _url = user_settings.get("WISKI_URL", "")

    # TODO: wellicht later nog toevoegen?
    if _cache_database_db is None and not disable_cache_db:
        _cache_database_db = duckdb.connect(database=":memory:", read_only=False)
        # _cache_database_db.execute("INSTALL spatial;")
        # _cache_database_db.execute("LOAD spatial;")

    # combine all three into a Deps object
    deps = Deps(url=_url)
    # for now this is limited to the session
    deps.cache_database_db = _cache_database_db
    deps.object_type_shortname = user_settings.get("OBJECT_TYPE_SHORTNAME", None)
    return CtxWithDeps(deps)
