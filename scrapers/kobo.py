from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import re
import time
import chromedriver_autoinstaller
import os
from selenium import webdriver
import shutil
from scrapers.utils import get_isolated_driver
chromedriver_autoinstaller.install()  # isso baixa e coloca o chromedriver na PATH automaticamente

def search_kobo_ebooks(query, is_isbn=False):
    if is_isbn:
        query = query.replace("-", "").strip()
    query_lower = query.lower()

    results = []
    driver, user_data_dir = get_isolated_driver()
    url = (
        f"https://www.kobo.com/pt/pt/search?"
        f"query={query.replace(' ', '+')}&fclanguages=pt&pagenumber=1&fcmedia=Book"
    )
    print("Abrindo URL:", url)
    driver.get(url)

    time.sleep(3)  # Ajuste conforme necessário

    try:
        items = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="search-results-items"] > div[role="listitem"]')

        for i, item in enumerate(items[:10]):
            try:
                title_elem = item.find_element(By.CSS_SELECTOR, '[data-testid="title"] .link--label')
                title = title_elem.text.strip() or title_elem.get_attribute("textContent").strip()

                author_elem = item.find_element(By.CSS_SELECTOR, '[data-testid="authors"] .link--label')
                author = author_elem.text.strip() or author_elem.get_attribute("textContent").strip()

                # Preço (procura pelo span com data-testid correto)
                raw_price = "Indisponível"
                price_spans = item.find_elements(By.CSS_SELECTOR, 'span')
                for sp in price_spans:
                    data_testid = sp.get_attribute('data-testid')
                    if data_testid and data_testid.endswith('-pricing-price-value'):
                        raw_price = sp.text.strip()
                        break  # usa o primeiro encontrado

                # Filtro: ignora se não encontrar a query no título ou autor
                if query_lower not in title.lower() and query_lower not in author.lower():
                    continue

                link = title_elem.get_attribute("href")

                try:
                    cover_elem = item.find_element(By.CSS_SELECTOR, 'div[data-testid="book-cover-container"] img')
                    cover_url = cover_elem.get_attribute("src")
                except NoSuchElementException:
                    cover_url = ""

                results.append({
                    "store": "Kobo",
                    "title": title,
                    "author": author,
                    "priceStr": raw_price,
                    "link": link,
                    "cover": cover_url
                })

            except Exception as e:
                print(f"⚠️ Erro ao processar item {i} da Kobo:", e)

    except Exception as e:
        print("❌ Erro ao buscar resultados da Kobo:", e)

    finally:
        driver.quit()
        shutil.rmtree(user_data_dir, ignore_errors=True)

    return results



def get_price_from_url(url: str, is_ebook: bool = False) -> float | None:
    """
    Abre diretamente a página do produto (livro físico ou ebook) e extrai o preço atual.
    Retorna o preço como float, ou None se não encontrar.
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By

    driver, user_data_dir = get_isolated_driver()
    try:
        driver.get(url)

        # Aguarda carregamento
        driver.implicitly_wait(5)

        # Identifica o seletor correto conforme o tipo de produto
        if is_ebook:
            # Preço do ebook (geralmente na mesma div do físico, mas em páginas separadas)
            price_spans = driver.find_elements(By.CSS_SELECTOR, 'span')
            for sp in price_spans:
                data_testid = sp.get_attribute('data-testid')
                if data_testid and data_testid.endswith('-pricing-price-value'):
                    price_elem = sp.text.strip()

        price_str = price_elem.text.strip().replace("€", "").replace(",", ".")
        return float(price_str)

    except Exception as e:
        print("⚠️ Erro ao obter preço do Kobo:", e)
        return None

    finally:
        driver.quit()
        shutil.rmtree(user_data_dir, ignore_errors=True)


# Teste isolado
if __name__ == "__main__":
    livros = search_kobo_ebooks("saramago")
    for livro in livros:
        print(livro)
