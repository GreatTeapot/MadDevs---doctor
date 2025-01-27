import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from common.models.base import Base
from core.config import settings
from core.database import engine_async
from main import app


@pytest.fixture(scope="session", autouse=True)
def check_pytest_debug():
    pytest_debug = settings.db.pytest_debug
    if not pytest_debug:
        pytest.exit("PYTEST_DEBUG is not set to True, skipping tests.")



Base.metadata.bind = engine_async


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_async.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_async.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)




@pytest_asyncio.fixture
async def ac() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_test_client:
        yield async_test_client
