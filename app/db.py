from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

import logging

logger = logging.getLogger("uvicorn.error")

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/embeddings_db")
engine = create_async_engine(DATABASE_URL, future=True, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def get_db():
    print("get_db function called")  # Add this line
    async with SessionLocal() as session:
        logger.info(f"Yielding session: {type(session)}")
        try:
            yield session
        finally:
            await session.close()
