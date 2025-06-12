# backend/api/routes/user_dashboard.py

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from auth_funcs import current_active_user  # já importado do FastAPI Users
from book_models import User, TrackedBook
from sqlalchemy.future import select
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/dashboard", response_class=HTMLResponse)
async def user_dashboard(
    request: Request,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(TrackedBook).where(TrackedBook.user_id == user.id)
    )
    books = result.scalars().all()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "user_books": books  # passa para o Jinja
    })
