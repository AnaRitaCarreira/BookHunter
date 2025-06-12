from services.aggregator import search_all_sites, search_all_sites_ebooks
from core.email import send_price_alert  # (precisa ser criado)
from schemas import BookCreate  # book info com título, url, etc.
from book_models import get_all_tracked_books  # Ex: ORM ou mock
from database import AsyncSessionLocal
from sqlalchemy.future import select
from book_models import TrackedBook, User
from database import get_async_session
from core.email import send_price_alert  # importa a função que envia o e-mail
from scrapers import wook, bertrand, kobo,fnac  # importa o módulo wook.py
from urllib.parse import urlparse
# Mock do banco de dados em memória
user_book_prices = {}  # ex: {("user@email.com", "isbn123"): 18.90}

async def check_price_periodically(book_data: BookCreate):
    """
    Verifica o preço atual do livro e compara com o anterior salvo no banco.
    Se o preço caiu, envia email ao usuário.
    """
    search_term = book_data.title or book_data.isbn or book_data.store_url
    if not search_term:
        return  # Sem dados suficientes

    try:
        if book_data.is_ebook == True:
            results = await search_all_sites_ebooks(search_term, is_isbn=bool(book_data.isbn))
        elif book_data.is_ebook == False:
            results = await search_all_sites(search_term, is_isbn=bool(book_data.isbn))

        if not results:
            return

        prices = [float(book["price"]) for book in results if book.get("price")]
        if not prices:
            return

        current_price = min(prices)

        # Acessar banco
        async with get_async_session() as session:
            result = await session.execute(
                select(TrackedBook).where(
                    TrackedBook.title == book_data.title,
                    TrackedBook.author == book_data.author,
                    TrackedBook.user.has(email=book_data.user_email)
                )
            )
            tracked = result.scalars().first()

            if not tracked:
                return

            # Compara preço atual com o salvo
            if tracked.current_price is not None and current_price < tracked.current_price:
                # Preço caiu → envia alerta
                await send_price_alert(
                    to_email=book_data.user_email,
                    book_title=book_data.title,
                    old_price=tracked.current_price,
                    new_price=current_price,
                    store=tracked.store or "a loja",
                    link=tracked.store_url
                )
                tracked.previous_price = tracked.current_price
                tracked.current_price = current_price
                await session.commit()

            elif tracked.current_price != current_price:
                # Preço mudou (mas não caiu) → apenas atualiza
                tracked.previous_price = tracked.current_price
                tracked.current_price = current_price
                await session.commit()

    except Exception as e:
        print(f"[tracker] Erro ao verificar preço: {e}")




async def get_all_tracked_books(session):
    result = await session.execute(select(TrackedBook))
    return result.scalars().all()


async def check_all_tracked_books():
    async with get_async_session() as session:
        result = await session.execute(select(TrackedBook).join(User))
        books = result.scalars().all()

        for book in books:
            new_price = await get_price_by_store(book.store, book.store_url, book.is_ebook)

            if new_price is not None and new_price < book.current_price:
                # Atualiza no banco
                book.current_price = new_price
                await session.commit()

                # Envia alerta
                result = await session.execute(
                    select(User).where(User.id == book.user_id)
                )
                user = result.scalar_one_or_none()
                if user and user.email:
                    send_price_alert(user.email, book.title, new_price, book.store_url)


# services/price_fetcher.py



def get_price_by_store(store: str, url: str, is_ebook: bool) -> float | None:
    if "wook" in store.lower() or "wook.pt" in url:
        return wook.get_price_from_url(url, is_ebook=is_ebook)
    elif "bertrand" in store.lower() or "bertrand.pt" in url: 
        return bertrand.get_price_from_url(url, is_ebook=is_ebook)
    elif "fnac" in store.lower() or "fnac.pt" in url: 
        return fnac.get_price_from_url(url, is_ebook=is_ebook)
    elif "kobo" in store.lower() or "kobo.pt" in url: 
        return kobo.get_price_from_url(url, is_ebook=is_ebook)  
    else:
        print(f"⚠️ Loja não suportada ainda: {store}")
        return None
