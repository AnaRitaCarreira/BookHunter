from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from base import Base
from passlib.hash import bcrypt
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.db import SQLAlchemyUserDatabase
from pydantic import BaseModel, EmailStr
from fastapi_users import schemas

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.orm import relationship


class TrackedBook(Base):
    __tablename__ = "tracked_books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=True)
    cover = Column(String, nullable=True)              # Adicionado
    store = Column(String, nullable=True)              # Adicionado
    store_url = Column(String, nullable=False)
    isbn = Column(String, nullable=True)               # Adicionado
    current_price = Column(Float, nullable=True)
    previous_price = Column(Float, nullable=True)
    is_ebook = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="tracked_books")  # Relacionamento bidirecional (opcional)



"""
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    def verify_password(self, password: str):
        return bcrypt.verify(password, self.hashed_password)"""


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"  # Nome consistente com ForeignKey acima

    name = Column(String(100), nullable=False)
    id = Column(Integer, primary_key=True)  # ✅ DEFINA A CHAVE PRIMÁRIA
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    # Optional: relacionamento com os livros
    tracked_books = relationship("TrackedBook", back_populates="user")


async def get_all_tracked_books(session: AsyncSession):
    result = await session.execute(select(TrackedBook))
    books = result.scalars().all()
    return books




