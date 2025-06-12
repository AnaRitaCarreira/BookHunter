from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re
import time


def search_kobo_ebooks(query, is_isbn=False):
    if is_isbn:
        query = query.replace("-", "").strip()
    query_lower = query.lower()
    # Caminho para o navegador Brave e o ChromeDriver
    brave_path = r"C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    chromedriver_path = r"./chromedriver-linux64/chromedriver"

    # Configurações do Selenium
    options = Options()
    options.binary_location = brave_path
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless")  # Remova esta linha se quiser ver o navegador
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # Monta a URL de busca
    url = f"https://www.kobo.com/pt/pt/search?query={query.replace(' ', '+')}&fclanguages=pt&pagenumber=1&fcmedia=Book"
    print("Abrindo URL:", url)
    driver.get(url)

    time.sleep(3)  # Aguarda carregar os resultados, aumente se necessário

    results = []

    try:
        # Localiza os itens da busca
        items = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="search-results-items"] > div[role="listitem"]')

        for item in items[:10]:  # Limita aos primeiros 10 resultados

            # Procurar TÍTULO
            title = None
            try:
                title_elem = item.find_element(By.CSS_SELECTOR, '[data-testid="title"] .link--label')
                title = title_elem.text.strip()
                if not title:
                    title = title_elem.get_attribute("textContent").strip()
            except Exception as e:
                print("Erro ao extrair título:", e)

            # Procurar AUTOR
            author = None
            try:
                author_elem = item.find_element(By.CSS_SELECTOR, '[data-testid="authors"] .link--label')
                author = author_elem.text.strip()
                if not author:
                    author = author_elem.get_attribute("textContent").strip()
            except Exception as e:
                print("Erro ao extrair autor:", e)
            

            # Preço
            price_spans = item.find_elements(By.CSS_SELECTOR, 'span')
            for sp in price_spans:
                data_testid = sp.get_attribute('data-testid')
                if data_testid and data_testid.endswith('-pricing-price-value'):
                    raw_price = sp.text.strip()
                    #print(f"Preço encontrado no item: {raw_price}")
            # Filtro simples para conter a query no título ou autor
            if query_lower not in title.lower() and query_lower not in author.lower():
                continue

            link = item.find_element(By.CSS_SELECTOR, 'a[data-testid="title"]').get_attribute("href")
            cover_url = item.find_element(By.CSS_SELECTOR, 'div[data-testid="book-cover-container"] img').get_attribute("src")

            # Capa
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
        print("Erro geral ao buscar resultados:", e)

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


# Teste isolado
if __name__ == "__main__":
    livros = search_kobo_ebooks("saramago")
    for livro in livros:
        print(livro)
