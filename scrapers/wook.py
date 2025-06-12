from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from urllib.parse import quote
import time

def search_wook(query, is_isbn=False):

    # Se for ISBN, pode tratar para evitar espaços etc.
    if is_isbn:
        query = query.replace("-", "").strip()

    brave_path = r"C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    chromedriver_path = r"./chromedriver-win64/chromedriver.exe"

    options = Options()
    options.binary_location = brave_path
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # A URL de busca é a mesma para q e isbn no wook, então apenas usa o query direto
    url = f"https://www.wook.pt/pesquisa?keyword={quote(query)}&search-disposition=list&select%5Btip_art_web_id%5D=122&page=1&sort=ranking_orderSort%7Casc&interval%5Bpre_ven_cap%5D="
    print("Abrindo URL:", url)
    driver.get(url)
    

    results = []
    items = driver.find_elements(By.CSS_SELECTOR, "li.product.d-flex")

    if items:
        for item in items[:10]:
            try:
                title = item.find_element(By.CSS_SELECTOR, ".title a span.font-bold").text.strip()
                author = item.find_element(By.CSS_SELECTOR, ".authors a").text.strip().replace("de ", "")

                # Tentativa segura de obter o preço
                try:
                    price = item.find_element(By.CSS_SELECTOR, ".pvp-discount span.font-bold").text.strip()
                except NoSuchElementException:
                    price = "Indisponível"  # Ou None, ou "" dependendo da tua preferência

                link = item.find_element(By.CSS_SELECTOR, ".title a").get_attribute("href")
                cover = item.find_element(By.CSS_SELECTOR, "a.cover img")
                cover_url = cover.get_attribute("data-src") or cover.get_attribute("src")

                results.append({
                    "store": "Wook",
                    "title": title,
                    "author": author,
                    "priceStr": price,
                    "link": f"https://www.wook.pt{link}" if link.startswith("/") else link,
                    "cover": cover_url
                })


            except Exception as e:
                print("⚠️ Erro ao processar um item:", e)
                print(item.get_attribute("outerHTML"))
    else:
        # Página única do produto
        try:
            title = driver.find_element(By.CSS_SELECTOR, "h1.font-medium span.title").text.strip()
            author = driver.find_element(By.CSS_SELECTOR, "span.authors a").text.strip()
            price = driver.find_element(By.CSS_SELECTOR, "#product-price span.price").text.strip()
            link = driver.current_url
            cover = driver.find_element(By.CSS_SELECTOR, ".image-container picture img").get_attribute("src")

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

    driver.quit()
    return results

def search_wook_ebooks(query, is_isbn=False):

    # Se for ISBN, pode tratar para evitar espaços etc.
    if is_isbn:
        query = query.replace("-", "").strip()

    brave_path = r"C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    chromedriver_path = r"./chromedriver-win64/chromedriver.exe"

    options = Options()
    options.binary_location = brave_path
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # A URL de busca é a mesma para q e isbn no wook, então apenas usa o query direto
    url = f"https://www.wook.pt/pesquisa?keyword={quote(query)}&search-disposition=list&select[tip_art_web_id]=619&page=1&sort=ranking_orderSort|asc&interval[pre_ven_cap]="
    print("Abrindo URL:", url)
    driver.get(url)
    

    results = []
    items = driver.find_elements(By.CSS_SELECTOR, "li.product.d-flex")
    #print("Numero de items", len(items))
    if items:
        # Página de lista
        for item in items[:10]:
            try:
                title = item.find_element(By.CSS_SELECTOR, ".title a span.font-bold").text.strip()
                author = item.find_element(By.CSS_SELECTOR, ".authors a").text.strip().replace("de ", "")
                price = item.find_element(By.CSS_SELECTOR, ".pvp-discount span.font-bold").text.strip()
                link = item.find_element(By.CSS_SELECTOR, ".title a").get_attribute("href")
                cover = item.find_element(By.CSS_SELECTOR, "a.cover img").get_attribute("data-src") or \
                        item.find_element(By.CSS_SELECTOR, "a.cover img").get_attribute("src")
                
                results.append({
                    "store": "Wook",
                    "title": title,
                    "author": author,
                    "priceStr": price,
                    "link": f"https://www.wook.pt{link}" if link.startswith("/") else link,
                    "cover": cover
                })
            except Exception as e:
                print("Erro item lista:", e)
    else:
        # Página única do produto
        try:
            title = driver.find_element(By.CSS_SELECTOR, "h1.font-medium span.title").text.strip()
            author = driver.find_element(By.CSS_SELECTOR, "span.authors a").text.strip()
            price = driver.find_element(By.CSS_SELECTOR, "#product-price span.price").text.strip()
            link = driver.current_url
            cover = driver.find_element(By.CSS_SELECTOR, ".image-container picture img").get_attribute("src")

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
    chromedriver_path = r"./chromedriver-win64/chromedriver.exe"

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
