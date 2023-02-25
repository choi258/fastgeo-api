import asyncio
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import config
from app.core.session import async_engine, async_session
from app.main import app
from app.models import Base, Atm

default_atm_id = 21634
default_atm_addr = "333 Han"
default_atm_prov = "ab"



@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_db_setup_sessionmaker():
    # assert if we use TEST_DB URL for 100%
    assert config.settings.ENVIRONMENT == "PYTEST"

    # always drop and create test db tables between tests session
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(autouse=True)
async def session(test_db_setup_sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

        # delete all data from all tables after test
        for name, table in Base.metadata.tables.items():
            await session.execute(delete(table))
        await session.commit()


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        client.headers.update({"Host": "localhost"})
        yield client


@pytest_asyncio.fixture
async def default_atm(test_db_setup_sessionmaker) -> Atm:
    async with async_session() as session:
        result = await session.execute(
            select(Atm).where(Atm.id == default_atm_id)
        )
        atm = result.scalars().first()
        if atm is None:
            new_atm = Atm(
                id=default_atm_id,
                address=default_atm_addr,
                provider=default_atm_prov
            )
            new_atm.id = default_atm_id
            session.add(new_atm)
            await session.commit()
            await session.refresh(new_atm)
            return new_atm
        return atm
