# user_manager.py
from fastapi_users.manager import BaseUserManager
from fastapi import Depends
from config import SECRET_KEY
from fastapi_users.db import SQLAlchemyUserDatabase
from book_models import User
from database import get_async_session
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession


class UserManager(BaseUserManager[User, int]):
    user_db_model = User
    reset_password_token_secret = SECRET_KEY
    verification_token_secret = SECRET_KEY

    def parse_id(self, user_id: str) -> int:
        return int(user_id)
    
    async def on_after_register(self, user: User, request=None):
        print(f"Novo usuário registrado: {user.email}")

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
