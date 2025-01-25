import pytest
from httpx import AsyncClient
from tests.confest import ac

from tests.unit.data.patient_data import create_patient_data, update_patient_data
from tests.unit.utils.auth_util import get_access_token
from tests.unit.utils.test_utils import validate_response_data

@pytest.mark.asyncio
@pytest.mark.parametrize("case", create_patient_data)
async def test_create_patient(ac: AsyncClient, case):
    access_token = await get_access_token(ac, "doctor_user", "ValidPass123")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await ac.post("/api/v1/patient/", json=case, headers=headers)
    validate_response_data(response, case["expected_status"])

@pytest.mark.asyncio
@pytest.mark.parametrize("case", update_patient_data)
async def test_update_patient(ac: AsyncClient, case):
    access_token = await get_access_token(ac, "doctor_user", "ValidPass123")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await ac.put(f"/api/v1/patient/{case['patient_id']}", json=case, headers=headers)
    validate_response_data(response, case["expected_status"])
