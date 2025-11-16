from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker
from app.config import settings
from app.core.utils import BASE_DIR

if settings.DEBUG:
    SQLALCHEMY_ASYNC_DATABASE_URL = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite"
else:
    SQLALCHEMY_ASYNC_DATABASE_URL = f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'
if settings.DEBUG:
    SQLALCHEMY_DATABASE_URL = f'sqlite:///{BASE_DIR}/db.sqlite'
else:
    SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'

engine: Engine = create_engine(SQLALCHEMY_DATABASE_URL)

engine_async: AsyncEngine = create_async_engine(
    SQLALCHEMY_ASYNC_DATABASE_URL,
    pool_size=20,
    max_overflow=20,
    pool_timeout=30,
    pool_pre_ping=True,
    echo=False
)
AsyncSessionLocal = async_sessionmaker(
    bind=engine_async,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def get_async_db()-> AsyncGenerator[AsyncSession | Any, Any]:
    async with AsyncSessionLocal() as session:
        yield session

@asynccontextmanager
async def get_db_context():
    async with AsyncSessionLocal() as session:
        yield session

