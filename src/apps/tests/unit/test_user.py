import pytest
from httpx import AsyncClient

from tests.unit.data.user_data import register_data
from tests.unit.utils.test_utils import validate_response_data


@pytest.mark.asyncio
@pytest.mark.parametrize("case", register_data)
async def test_register_user(ac: AsyncClient, case):
    response = await ac.post("/api/v1/user/register", json=case)
    validate_response_data(response, case["expected_status"])

