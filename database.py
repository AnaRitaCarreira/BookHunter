# /database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL
from sqlalchemy.future import select
from book_models import User 
from base import Base

# Criar o engine assíncrono com aiosqlite
engine = create_async_engine(DATABASE_URL, echo=True)

# Session assíncrona
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session



async def get_user_by_email(email: str, db: AsyncSession):
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
