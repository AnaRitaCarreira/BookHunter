from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import chromedriver_autoinstaller
from urllib.parse import quote
import time
import os
import shutil
from scrapers.utils import get_isolated_driver
chromedriver_autoinstaller.install()  # isso baixa e coloca o chromedriver na PATH automaticamente


def search_bertrand(query, is_isbn=False):
    if is_isbn:
        query = query.replace("-", "").strip()

    driver = None
    user_data_dir = None
    results = []

    try:
        driver, user_data_dir = get_isolated_driver()
        url = f"https://www.bertrand.pt/pesquisa/{query.replace(' ', '+')}/+/+/+/eyJ0aXBfYXJ0X3dlYl9pZCI6eyJpZCI6IjEyMiIsIm5hbWUiOiJMaXZybyJ9fQ"
        print("Abrindo URL:", url)
        driver.get(url)

        items = driver.find_elements(By.CSS_SELECTOR, "div.product-portlet")

        for i, item in enumerate(items[:10]):
            try:
                title_elem = item.find_element(By.CSS_SELECTOR, ".title-lnk")
                title = title_elem.text.strip()
                link = title_elem.get_attribute("href")

                try:
                    author = item.find_element(By.CSS_SELECTOR, ".authors p a").text.strip()
                except NoSuchElementException:
                    author = ""

                try:
                    price = item.find_element(By.CSS_SELECTOR, ".price .active-price").text.strip()
                except NoSuchElementException:
                    price = "Indisponível"

                try:
                    cover_img = item.find_element(By.CSS_SELECTOR, "div.cover a picture img")
                    cover_url = cover_img.get_attribute("src") or ""
                except NoSuchElementException:
                    cover_url = ""

                results.append({
                    "store": "Bertrand",
                    "title": title,
                    "author": author,
                    "priceStr": price,
                    "link": link,
                    "cover": cover_url
                })

            except Exception as e:
                print(f"⚠️ Erro ao extrair item {i} da Bertrand:", e)
                # print("HTML do item:", item.get_attribute('outerHTML'))

    except Exception as e:
        print("❌ Erro ao iniciar navegação Bertrand:", e)

    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
        if user_data_dir:
            shutil.rmtree(user_data_dir, ignore_errors=True)

    return results


def search_bertrand_ebooks(query, is_isbn=False):
    if is_isbn:
        query = query.replace("-", "").strip()

    driver = None
    user_data_dir = None
    results = []

    try:
        driver, user_data_dir = get_isolated_driver()
        url = (
            "https://www.bertrand.pt/pesquisa/"
            f"{query.replace(' ', '+')}/+/+/+/"
            "eyJ0aXBfYXJ0X3dlYl9pZCI6eyJpZCI6IjYxOSIsIm5hbWUiOiJlQm9vayJ9fQ"
        )
        print("Abrindo URL:", url)
        driver.get(url)

        items = driver.find_elements(By.CSS_SELECTOR, "div.product-portlet")

        for i, item in enumerate(items[:10]):
            try:
                title_elem = item.find_element(By.CSS_SELECTOR, ".title-lnk")
                title = title_elem.text.strip()
                link = title_elem.get_attribute("href")

                try:
                    author = item.find_element(By.CSS_SELECTOR, ".authors p a").text.strip()
                except NoSuchElementException:
                    author = ""

                try:
                    price = item.find_element(By.CSS_SELECTOR, ".price .active-price").text.strip()
                except NoSuchElementException:
                    price = "Indisponível"

                try:
                    cover_img = item.find_element(By.CSS_SELECTOR, "div.cover a picture img")
                    cover_url = cover_img.get_attribute("src") or ""
                except NoSuchElementException:
                    cover_url = ""

                results.append({
                    "store": "Bertrand",
                    "title": title,
                    "author": author,
                    "priceStr": price,
                    "link": link,
                    "cover": cover_url
                })

            except Exception as e:
                print(f"⚠️ Erro ao extrair item {i} da Bertrand eBooks:", e)

    except Exception as e:
        print("❌ Erro ao iniciar navegação Bertrand eBooks:", e)

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
            price_elem = driver.find_element(By.CSS_SELECTOR, ".price .active-price").text.strip()
        else:
            # Livro físico — o mesmo seletor costuma funcionar
            price_elem = driver.find_element(By.CSS_SELECTOR, ".price .active-price").text.strip()




        price_str = price_elem.text.strip().replace("€", "").replace(",", ".")
        return float(price_str)

    except Exception as e:
        print("⚠️ Erro ao obter preço da Bertrand:", e)
        return None

    finally:
        driver.quit()
        shutil.rmtree(user_data_dir, ignore_errors=True)


# Teste isolado
if __name__ == "__main__":
    livros = search_bertrand("saramago")
    for livro in livros:
        print(livro)
