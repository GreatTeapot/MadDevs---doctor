import asyncio
import os
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from common.models.base import Base
from core.config import settings
from core.database import engine_async, async_session_maker
from main import app

load_dotenv(dotenv_path=".env")

def check_pytest_debug():
    pytest_debug = settings.db.pytest_debug
    if not pytest_debug:
        pytest.exit("PYTEST_DEBUG is not set to True, skipping tests.")



Base.metadata.bind = engine_async


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

@pytest_asyncio.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_async.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_async.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

app.dependency_overrides[override_get_async_session] = override_get_async_session


# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def ac() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_test_client:
        yield async_test_client

