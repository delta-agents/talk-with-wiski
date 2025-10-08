import json
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_ai import RunContext
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


def get_runtime_ctx() -> RunContext:
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
        _url = os.environ.get("WEB_SERVICE_URL", "http://vpweb600.wsbd.nl:8080/KiWIS/")

    # TODO: later nog toevoegen
    if _cache_database_db is None and not disable_cache_db:
        _cache_database_db = duckdb.connect(database=":memory:", read_only=False)
        _cache_database_db.execute("INSTALL spatial;")
        _cache_database_db.execute("LOAD spatial;")

    # combine all three into a Deps object
    deps = Deps(url=_url)
    # for now this is limited to the session
    deps.cache_database_db = _cache_database_db
    return CtxWithDeps(deps)
