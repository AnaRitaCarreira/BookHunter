from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from urllib.parse import quote
import time

def search_bertrand(query, is_isbn=False):
    # Se for ISBN, pode tratar para evitar espaços etc.
    if is_isbn:
        query = query.replace("-", "").strip()

    brave_path = r"C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    chromedriver_path = r"./chromedriver-linux64/chromedriver"

    options = Options()
    options.binary_location = brave_path
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    url = f"https://www.bertrand.pt/pesquisa/{query.replace(' ', '+')}/+/+/+/eyJ0aXBfYXJ0X3dlYl9pZCI6eyJpZCI6IjEyMiIsIm5hbWUiOiJMaXZybyJ9fQ"
    print("Abrindo URL:", url)
    driver.get(url)
    

    results = []
    items = driver.find_elements(By.CSS_SELECTOR, "div.product-portlet")



    results = []
    items = driver.find_elements(By.CSS_SELECTOR, "div.product-portlet")

    for item in items[:10]:
        try:
            title_elem = item.find_element(By.CSS_SELECTOR, ".title-lnk")
            title = title_elem.text
            link = title_elem.get_attribute("href")
            
            author = ""
            try:
                author = item.find_element(By.CSS_SELECTOR, ".authors p a").text
            except:
                pass
            try:
                price = item.find_element(By.CSS_SELECTOR, ".price .active-price").text
            except NoSuchElementException:
                price = "Indisponível"  # Ou None, ou "" dependendo da tua preferência

            cover_url = ""
            try:
                cover_img = item.find_element(By.CSS_SELECTOR, "div.cover a picture img")
                cover_url = cover_img.get_attribute("src")
            except:
                pass

            results.append({
                "store":"Bertrand",
                "title": title,
                "author": author,
                "priceStr": price,
                "link": link,
                "cover": cover_url
            })
        except Exception as e:
            print("Erro ao extrair item:", e)
            #print("HTML do item:", item.get_attribute('outerHTML'))

    driver.quit()
    return results


def search_bertrand_ebooks(query, is_isbn=False):
    # Se for ISBN, pode tratar para evitar espaços etc.
    if is_isbn:
        query = query.replace("-", "").strip()

    brave_path = r"C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    chromedriver_path = r"./chromedriver-linux64/chromedriver"

    options = Options()
    options.binary_location = brave_path
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    url = f"https://www.bertrand.pt/pesquisa/{query.replace(' ', '+')}/+/+/+/eyJ0aXBfYXJ0X3dlYl9pZCI6eyJpZCI6IjYxOSIsIm5hbWUiOiJlQm9vayJ9fQ"
    print("Abrindo URL:", url)
    driver.get(url)
    

    results = []
    items = driver.find_elements(By.CSS_SELECTOR, "div.product-portlet")



    results = []
    items = driver.find_elements(By.CSS_SELECTOR, "div.product-portlet")

    for item in items[:10]:
        try:
            title_elem = item.find_element(By.CSS_SELECTOR, ".title-lnk")
            title = title_elem.text
            link = title_elem.get_attribute("href")
            
            author = ""
            try:
                author = item.find_element(By.CSS_SELECTOR, ".authors p a").text
            except:
                pass
            try:
                price = item.find_element(By.CSS_SELECTOR, ".price .active-price").text
            except NoSuchElementException:
                price = "Indisponível"  # Ou None, ou "" dependendo da tua preferência

            cover_url = ""
            try:
                cover_img = item.find_element(By.CSS_SELECTOR, "div.cover a picture img")
                cover_url = cover_img.get_attribute("src")
            except:
                pass

            results.append({
                "store":"Bertrand",
                "title": title,
                "author": author,
                "priceStr": price,
                "link": link,
                "cover": cover_url
            })
        except Exception as e:
            print("Erro ao extrair item:", e)
            #print("HTML do item:", item.get_attribute('outerHTML'))

    driver.quit()
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

    brave_path = r"C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    chromedriver_path = r"./chromedriver-linux64/chromedriver"

    options = Options()
    options.binary_location = brave_path
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

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


# Teste isolado
if __name__ == "__main__":
    livros = search_bertrand("saramago")
    for livro in livros:
        print(livro)
