from scrapers.wook import search_wook, search_wook_ebooks
from scrapers.kobo import search_kobo_ebooks
from scrapers.bertrand import search_bertrand, search_bertrand_ebooks
from scrapers.fnac import search_fnac
import asyncio

import re

def parse_price(price_str):
    #print("💶 Preço bruto extraído:", price_str)  # Debug original
    
    if not price_str:
        #print("⚠️ Preço ausente ou vazio.")
        return None

    # Limpeza básica
    cleaned = price_str.strip().replace("€", "").replace("EUR", "").strip()
    #print("🧹 Preço após limpeza:", cleaned)

    # Regex para extrair número com vírgula ou ponto
    match = re.search(r"(\d+[.,]?\d*)", cleaned)
    if not match:
        #print("❌ Nenhum número reconhecido no preço.")
        return None

    num_str = match.group(1).replace(",", ".")
    #print("🔢 String numérica final:", num_str)

    try:
        parsed = float(num_str)
        #print("📊 Preço numérico convertido:", parsed)
        return parsed
    except Exception as e:
        #print("💥 Erro ao converter para float:", e)
        return None

    
async def search_all_sites(query: str, is_isbn: bool = False):
    # Dispara todas as buscas síncronas em threads paralelos
    tasks = [
        asyncio.to_thread(search_wook, query, is_isbn),
        asyncio.to_thread(search_bertrand, query, is_isbn),
        asyncio.to_thread(search_fnac, query, is_isbn), 
    ]

    results_lists = await asyncio.gather(*tasks)  # roda em paralelo

    # Junta todos os resultados numa lista só
    all_results = []
    for rlist in results_lists:
        all_results.extend(rlist)

    # Filtra resultados com preço válido
    filtered = []
    for r in all_results:
        price_num = parse_price(r.get("priceStr", ""))
        if price_num is not None:
            r["price"] = price_num
            filtered.append(r)

    return sorted(filtered, key=lambda x: x["price"])

async def search_all_sites_ebooks(query: str, is_isbn: bool = False):
    tasks = [
        asyncio.to_thread(search_wook_ebooks, query, is_isbn),
        asyncio.to_thread(search_bertrand_ebooks, query, is_isbn),
        asyncio.to_thread(search_kobo_ebooks, query, is_isbn), 
    ]

    results_lists = await asyncio.gather(*tasks)
    
    #for i, rlist in enumerate(results_lists):
        #print(f"Site {i} retornou {len(rlist)} resultados")

    all_results = []
    for rlist in results_lists:
        all_results.extend(rlist)

    filtered = []
    for r in all_results:
        price_num = parse_price(r.get("priceStr", ""))
        if price_num is not None:
            r["price"] = price_num
            filtered.append(r)

    #print(f"Total após filtro de preços: {len(filtered)}")
    return sorted(filtered, key=lambda x: x["price"])
