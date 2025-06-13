from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import chromedriver_autoinstaller
from selenium.common.exceptions import WebDriverException
from urllib.parse import quote
import time
import os
from selenium import webdriver
import shutil
from scrapers.utils import get_isolated_driver
chromedriver_autoinstaller.install()  # isso baixa e coloca o chromedriver na PATH automaticamente

def search_wook(query, is_isbn=False):
    if is_isbn:
        query = query.replace("-", "").strip()

    driver = None
    user_data_dir = None
    results = []

    try:
        driver, user_data_dir = get_isolated_driver()
        url = f"https://www.wook.pt/pesquisa?keyword={quote(query)}&search-disposition=list&select%5Btip_art_web_id%5D=122&page=1&sort=ranking_orderSort%7Casc"
        print("Abrindo URL:", url)
        driver.get(url)

        items = driver.find_elements(By.CSS_SELECTOR, "li.product.d-flex")

        if items:
            for i, item in enumerate(items[:10]):
                try:
                    title = item.find_element(By.CSS_SELECTOR, ".title a span.font-bold").text.strip()
                    author = item.find_element(By.CSS_SELECTOR, ".authors a").text.strip().replace("de ", "")

                    try:
                        price = item.find_element(By.CSS_SELECTOR, ".pvp-discount span.font-bold").text.strip()
                    except NoSuchElementException:
                        price = "Indisponível"

                    link = item.find_element(By.CSS_SELECTOR, ".title a").get_attribute("href")
                    cover_elem = item.find_element(By.CSS_SELECTOR, "a.cover img")
                    cover_url = cover_elem.get_attribute("data-src") or cover_elem.get_attribute("src") or ""

                    results.append({
                        "store": "Wook",
                        "title": title,
                        "author": author,
                        "priceStr": price,
                        "link": f"https://www.wook.pt{link}" if link.startswith("/") else link,
                        "cover": cover_url
                    })

                except Exception as e:
                    print(f"⚠️ Erro ao processar item {i} da Wook:", e)
                    # print(item.get_attribute("outerHTML"))
        else:
            # Página única de produto
            try:
                title = driver.find_element(By.CSS_SELECTOR, "h1.font-medium span.title").text.strip()
                author = driver.find_element(By.CSS_SELECTOR, "span.authors a").text.strip()
                price = driver.find_element(By.CSS_SELECTOR, "#product-price span.price").text.strip()
                link = driver.current_url
                cover = driver.find_element(By.CSS_SELECTOR, ".image-container picture img").get_attribute("src") or ""

                results.append({
                    "store": "Wook",
                    "title": title,
                    "author": author,
                    "priceStr": price,
                    "link": link,
                    "cover": cover
                })
            except Exception as e:
                print("⚠️ Erro ao processar página de produto único da Wook:", e)

    except WebDriverException as e:
        print("Erro ao iniciar WebDriver (Wook):", e)

    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
        if user_data_dir:
            shutil.rmtree(user_data_dir, ignore_errors=True)

    return results

def search_wook_ebooks(query, is_isbn=False):
    if is_isbn:
        query = query.replace("-", "").strip()

    driver = None
    user_data_dir = None
    results = []

    try:
        driver, user_data_dir = get_isolated_driver()
        url = f"https://www.wook.pt/pesquisa?keyword={quote(query)}&search-disposition=list&select[tip_art_web_id]=619&page=1&sort=ranking_orderSort|asc"
        print("Abrindo URL:", url)
        driver.get(url)

        items = driver.find_elements(By.CSS_SELECTOR, "li.product.d-flex")

        if items:
            for i, item in enumerate(items[:10]):
                try:
                    title = item.find_element(By.CSS_SELECTOR, ".title a span.font-bold").text.strip()
                    author = item.find_element(By.CSS_SELECTOR, ".authors a").text.strip().replace("de ", "")

                    try:
                        price = item.find_element(By.CSS_SELECTOR, ".pvp-discount span.font-bold").text.strip()
                    except NoSuchElementException:
                        price = "Indisponível"

                    link = item.find_element(By.CSS_SELECTOR, ".title a").get_attribute("href")
                    cover_elem = item.find_element(By.CSS_SELECTOR, "a.cover img")
                    cover_url = cover_elem.get_attribute("data-src") or cover_elem.get_attribute("src") or ""

                    results.append({
                        "store": "Wook",
                        "title": title,
                        "author": author,
                        "priceStr": price,
                        "link": f"https://www.wook.pt{link}" if link.startswith("/") else link,
                        "cover": cover_url
                    })

                except Exception as e:
                    print(f"⚠️ Erro ao processar item {i} da lista Wook Ebooks:", e)

        else:
            # Página única
            try:
                title = driver.find_element(By.CSS_SELECTOR, "h1.font-medium span.title").text.strip()
                author = driver.find_element(By.CSS_SELECTOR, "span.authors a").text.strip()
                price = driver.find_element(By.CSS_SELECTOR, "#product-price span.price").text.strip()
                link = driver.current_url
                cover = driver.find_element(By.CSS_SELECTOR, ".image-container picture img").get_attribute("src") or ""

                results.append({
                    "store": "Wook",
                    "title": title,
                    "author": author,
                    "priceStr": price,
                    "link": link,
                    "cover": cover
                })
            except Exception as e:
                print("⚠️ Erro ao processar página de produto único (ebook Wook):", e)

    except WebDriverException as e:
        print("Erro ao iniciar WebDriver (Wook Ebooks):", e)

    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
        if user_data_dir:
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
            price_elem = driver.find_element(By.CSS_SELECTOR, "#product-price span.price").text.strip()
        else:
            # Livro físico — o mesmo seletor costuma funcionar
            price_elem = driver.find_element(By.CSS_SELECTOR, "#product-price span.price").text.strip()




        price_str = price_elem.text.strip().replace("€", "").replace(",", ".")
        return float(price_str)

    except Exception as e:
        print("⚠️ Erro ao obter preço da Wook:", e)
        return None

    finally:
        driver.quit()
        shutil.rmtree(user_data_dir, ignore_errors=True)
