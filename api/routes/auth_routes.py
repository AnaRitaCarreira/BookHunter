# api/routes/auth_routhes.py
from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi_users import FastAPIUsers
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.hash import bcrypt
from fastapi.responses import RedirectResponse
from fastapi.responses import Response
from fastapi import status
from database import get_async_session
from book_models import User
from auth.manager import auth_backend
from fastapi import Request, Form, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import EmailStr
from database import get_user_by_email
from core.email import send_reset_email, generate_reset_token
from core.email import verify_reset_token

router = APIRouter()

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(User, session)

fastapi_users = FastAPIUsers[User, int](get_user_db, [auth_backend])
current_user = fastapi_users.current_user()

@router.post("/auth/register")
async def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(User).where(User.email == email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já está registrado")


    hashed_password = bcrypt.hash(password)
    new_user = User(name=name, email=email, hashed_password=hashed_password)
    session.add(new_user)
    await session.commit()

    return {"message": "Conta criada com sucesso!"}


@router.post("/auth/logout")
def logout(response: Response):
    response.delete_cookie(key="fastapiusersauth")
    return {"msg": "Logout feito com sucesso"}



@router.post("/auth/password/reset-request")
async def password_reset_request(
    background_tasks: BackgroundTasks,
    email: EmailStr = Form(...),
    db: AsyncSession = Depends(get_async_session)  

):
    user = await get_user_by_email(email, db)
    if not user:
        return JSONResponse(status_code=400, content={"message": "Email não encontrado."})

    token = generate_reset_token(user.email)
    #reset_link = f"https://bookhunter.pt/reset_password?token={token}"
    reset_link = f"http://127.0.0.1:8000/reset_password.html?token={token}"

    background_tasks.add_task(send_reset_email, user.email, reset_link)
    return {"message": "Email de recuperação enviado."}


from pydantic import BaseModel

class PasswordResetRequest(BaseModel):
    token: str
    new_password: str

@router.post("/auth/password/reset")
async def reset_password(
    data: PasswordResetRequest,
    db: AsyncSession = Depends(get_async_session)
):
    email = verify_reset_token(data.token)
    if not email:
        raise HTTPException(status_code=400, detail="Token inválido ou expirado")

    user = await get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    hashed_password = bcrypt.hash(data.new_password)
    user.hashed_password = hashed_password

    db.add(user)
    await db.commit()

    return {"message": "Palavra-passe atualizada com sucesso"}

