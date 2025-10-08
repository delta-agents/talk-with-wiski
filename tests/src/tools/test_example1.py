import pytest

from talk_with_wiski.models.modelset_1.example1 import AddIndexInput, AddIndexOutput
from talk_with_wiski.routers.setup_connections import get_runtime_ctx
from talk_with_wiski.tools.toolset_1.example1 import add_index
from tests.utils_tests import setup_dot_env


@pytest.fixture
def test_context():
    """Create a test context with FEWS webservice URL"""
    setup_dot_env()
    return get_runtime_ctx()


@pytest.mark.asyncio
async def test_example1(test_context):
    """Test handling of invalid time ranges"""
    # Test end time before start time
    input = AddIndexInput(index=1)

    res: AddIndexOutput = await add_index(test_context, input)

    res.data
