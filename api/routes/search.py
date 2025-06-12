import re
from fastapi import APIRouter, Query, HTTPException
from services.aggregator import search_all_sites, search_all_sites_ebooks

router = APIRouter()

ISBN_REGEX = re.compile(r"^\d{10}(\d{3})?$")

@router.get("/search")
async def search_books(q: str = Query(..., min_length=3)):
    if not q:
        raise HTTPException(status_code=400, detail="O parâmetro 'q' é obrigatório.")

    is_isbn = bool(ISBN_REGEX.match(q.replace("-", "").strip()))
    search_term = q.strip()

    try:
        results = await search_all_sites(search_term, is_isbn=is_isbn)
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao buscar dados")

    return {
        "query": search_term,
        "is_isbn": is_isbn,
        "results": results
    }


@router.get("/search_ebooks")
async def search_ebooks(q: str = Query(..., min_length=3)):
    if not q:
        raise HTTPException(status_code=400, detail="O parâmetro 'q' é obrigatório.")

    is_isbn = bool(ISBN_REGEX.match(q.replace("-", "").strip()))
    search_term = q.strip()

    try:
        results = await search_all_sites_ebooks(search_term, is_isbn=is_isbn)
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao buscar dados")

    return {
        "query": search_term,
        "is_isbn": is_isbn,
        "results": results
    }
