from fastapi import APIRouter, BackgroundTasks, Depends
from schemas import BookCreate  # Assumindo que tens schemas.py com BookCreate
from  services.tracker import check_price_periodically  # função para tracking
from auth_funcs import current_active_user  # já importado do FastAPI Users
from book_models import User, TrackedBook
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from sqlalchemy.future import select
from fastapi import Body

router = APIRouter()

@router.post("/track")
async def add_to_tracking(
    book_data: BookCreate,
    background_tasks: BackgroundTasks,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    # Garante que o email do user logado é usado
    book_data.user_email = user.email

    # 1. Verifica se já está a ser seguido (evita duplicados)
    result = await session.execute(
        select(TrackedBook).where(
            TrackedBook.title == book_data.title,
            TrackedBook.author == book_data.author,
            TrackedBook.store == book_data.store,
            TrackedBook.store_url == book_data.store_url,
            TrackedBook.is_ebook == book_data.is_ebook,
            TrackedBook.user_id == user.id
        )
    )
    existing = result.scalars().first()
    if existing:
        return {"status": "already_tracking"}

    # 2. Cria novo registro no banco de dados
    new_book = TrackedBook(
        title=book_data.title,
        author=book_data.author,
        cover=book_data.cover,
        current_price=book_data.price,
        previous_price=book_data.price, 
        store=book_data.store,
        store_url=book_data.store_url,
        user_id=user.id,
        isbn=book_data.isbn,
        is_ebook=book_data.is_ebook
    )
    session.add(new_book)
    await session.commit()

    # 3. Adiciona tarefa em background para monitoramento de preços
    background_tasks.add_task(check_price_periodically, book_data)

    return {"status": "tracking started"}


@router.get("/track/tbr")
async def get_user_tbr(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(
        select(TrackedBook).where(TrackedBook.user_id == user.id)
    )
    books = result.scalars().all()
    return [
        {
            "title": book.title,
            "author": book.author,
            "cover": getattr(book, "cover", ""),
            "price": book.current_price,
            "store": getattr(book, "store", ""),
            "link": getattr(book, "store_url", ""),
            "is_ebook": getattr(book, "is_ebook", ""),
        }
        for book in books
    ]

@router.get("/track/check")
async def check_if_tracked(
    title: str, author: str,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(
        select(TrackedBook).where(
            TrackedBook.title == title,
            TrackedBook.author == author,
            TrackedBook.user_id == user.id
        )
    )
    book = result.scalars().first()
    return {"tracked": bool(book)}



@router.delete("/track/remove")
async def remove_from_tracking(
    payload: dict = Body(...),
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(TrackedBook).where(
        TrackedBook.title == payload["title"],
        TrackedBook.author == payload["author"],
        TrackedBook.store == payload["store"],
        TrackedBook.store_url == payload["store_url"],
        TrackedBook.user_id == user.id

    )
    result = await session.execute(stmt)
    book = result.scalars().first()
    if book:
        await session.delete(book)
        await session.commit()
        return {"status": "removed"}
    return {"status": "not_found"}
