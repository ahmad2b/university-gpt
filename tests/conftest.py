from collections.abc import Generator

import os
import sys
import pytest
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from fastapi.testclient import TestClient

from app.core.database import get_session
from app.app import create_app
from app.config import Settings 

from sqlmodel import Session


# Add the project directory to the path
sys.path.append(os.getcwd())

# Load environment variables
load_dotenv(find_dotenv())

# Database connection string
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# Create an asynchronous engine for the database
engine = create_async_engine(DATABASE_URL, echo=True,
    future=True,
    pool_size=20,
    max_overflow=20,
    pool_recycle=3600)

@pytest.fixture(scope="session")
async def async_db_session():
    """Fixture to provide a database session for tests, automatically handling context."""
    async_session = async_sessionmaker(engine, class_ = AsyncSession, expire_on_commit=False)
    # async with async_session() as session:
    #     yield session
    session = async_session()
    try:
        yield session
    finally:
        await session.close()
        

# --- Overrides the get_session dependency in the main.py file

@pytest.fixture(scope="module")
def client(async_db_session: AsyncSession) -> Generator[TestClient, None, None]:
    
    def override_get_session():
        return async_db_session
    
    test_settings = Settings()

    app = create_app(test_settings)

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as c:
        yield c 