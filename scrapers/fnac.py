from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import chromedriver_autoinstaller
import os
from selenium import webdriver
from utils import get_isolated_driver
chromedriver_autoinstaller.install()  # isso baixa e coloca o chromedriver na PATH automaticamente

def search_fnac(query, is_isbn=False):
    if is_isbn:
        query = query.replace("-", "").strip()

    driver, user_data_dir = get_isolated_driver()

    url = f"https://www.fnac.pt/SearchResult/ResultList.aspx??SCat=2!1&SDM=list&Search={query.replace(' ', '+')}&sft=1"
    print("Abrindo URL:", url)

    driver.get(url)
    wait = WebDriverWait(driver, 10)

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "article.Article-itemGroup")))
    except TimeoutException:
        print("Timeout esperando os artigos carregarem")
        driver.quit()
        shutil.rmtree(user_data_dir, ignore_errors=True)
        return []

    results = []
    items = driver.find_elements(By.CSS_SELECTOR, "article.Article-itemGroup")
    #print(f"Número de artigos encontrados: {items_count}")

    # Rebuscar o elemento no índice i para evitar stale element
    item = items[0]
    time.sleep(0.3)  # evita correr rápido demais e causar problemas

    title_elem = WebDriverWait(item, 5).until(
        EC.presence_of_element_located((By.XPATH, ".//a[contains(@class, 'js-Search-hashLink')]"))
    )
    title = title_elem.text
    link = title_elem.get_attribute("href")

    authors = []
    try:
        author_elements = item.find_elements(By.CSS_SELECTOR, ".Article-descSub a")
        authors = [a.text for a in author_elements]
    except Exception:
        pass

    try:
        price_old = item.find_element(By.CSS_SELECTOR, "del.oldPrice").text
    except NoSuchElementException:
        price_old = ""

    try:
        price_new = item.find_element(By.CSS_SELECTOR, "strong.userPrice").text
    except NoSuchElementException:
        price_new = ""

    cover_url = ""
    try:
        cover_img = item.find_element(By.CSS_SELECTOR, ".thumbnail-imgWrapper img")
        cover_url = cover_img.get_attribute("src")
    except Exception:
        pass

    results.append({
        "store": "Fnac",
        "title": title,
        "authors": authors,
        "price_old": price_old,
        "priceStr": price_new,
        "link": link,
        "cover": cover_url
    })
    #print("results:", results)
    #print(f"--- Item {0} --- OK")

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
        if is_ebook == False:
            # Preço do ebook (geralmente na mesma div do físico, mas em páginas separadas)
            price_elem = driver.find_element(By.CSS_SELECTOR, "span.userPrice").text.strip()

        price_str = price_elem.text.strip().replace("€", "").replace(",", ".")
        return float(price_str)

    except Exception as e:
        print("⚠️ Erro ao obter preço da Fnac:", e)
        return None

    finally:
        driver.quit()
        shutil.rmtree(user_data_dir, ignore_errors=True)


# Teste
if __name__ == "__main__":
    livros = search_fnac("filha da louca")
    for livro in livros:
        print(livro)
