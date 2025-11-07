import os
import pytest


from talk_with_wiski.tools import get_parametertype_list
from talk_with_wiski.models.modelset_retrieval.get_parametertype_list import (
    GetParametertypeListInput,
    GetParametertypeListOutput,
)
from talk_with_wiski.routers.setup_connections import get_runtime_ctx

from tests.utils_tests import setup_dot_env


@pytest.fixture
def test_context():
    """Create a test context with FEWS webservice URL"""
    setup_dot_env()
    return get_runtime_ctx()


@pytest.mark.skipif(
    os.getenv("GITHUB_ACTIONS") == "true",
    reason="Kan alleen lokaal getest worden",
)
@pytest.mark.asyncio
async def test_get_parametertype_list(test_context):
    """Test handling of invalid time ranges"""
    # Test end time before start time
    # input = GetParametertypeListInput(parametertype_name=['Evaporation','WNS*'])
    input = GetParametertypeListInput(parametertype_name=["Evaporation"])

    output: GetParametertypeListOutput = await get_parametertype_list(
        test_context, input
    )

    assert len(output.data) > 0  # by default
    assert "ParametertypeList obtained from KiWIS API" in output.description
