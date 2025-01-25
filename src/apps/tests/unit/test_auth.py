import pytest
from httpx import AsyncClient
from tests.confest import ac
from tests.unit.data.auth_data import login_data, logout_data
from tests.unit.utils.auth_util import get_access_token
from tests.unit.utils.test_utils import validate_response_data

@pytest.mark.asyncio
@pytest.mark.parametrize("case", login_data)
async def test_login(ac: AsyncClient, case):
    response = await ac.post("/api/v1/auth/login", json={"credentials": case["credentials"], "password": case["password"]})
    validate_response_data(response, case["expected_status"])

@pytest.mark.asyncio
async def test_logout(ac: AsyncClient):
    access_token = await get_access_token(ac, "valid_user", "ValidPass123")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await ac.post("/api/v1/auth/logout", headers=headers)
    validate_response_data(response, logout_data[0]["expected_status"], {"message": logout_data[0]["expected_message"]})
