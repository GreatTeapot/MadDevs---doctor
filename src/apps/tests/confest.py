import asyncio
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from common.models.base import Base
from core.config import settings
from core.database import async_session_maker, engine_async
from main import app


@pytest.fixture(scope="session", autouse=True)
def check_pytest_debug():
    pytest_debug = settings.db.pytest_debug
    if not pytest_debug:
        pytest.exit("PYTEST_DEBUG is not set to True, skipping tests.")


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

Base.metadata.bind = engine_async


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session



@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_async.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_async.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
