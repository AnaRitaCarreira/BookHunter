# auth_funcs.py
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTStrategy, AuthenticationBackend, CookieTransport
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi import Depends
from database import get_async_session
from book_models import User
from schemas import UserCreate, UserRead
from config import SECRET_KEY
from sqlalchemy.ext.asyncio import AsyncSession
from user_manager import get_user_manager

cookie_transport = CookieTransport(
    cookie_name="fastapiusersauth",
    cookie_max_age=3600,
    cookie_secure=False,  # em dev, desativa HTTPS-only - mudar para True quando estiver com HTTPS
    cookie_httponly=True,
    cookie_samesite="lax",  # ou "none" se frontend e backend forem domínios diferentes
)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


get_current_user = fastapi_users.current_user()

current_active_user = fastapi_users.current_user(active=True)
