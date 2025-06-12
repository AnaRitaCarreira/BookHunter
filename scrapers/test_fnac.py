from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def search_fnac(query):
    chrome_path = "/usr/bin/google-chrome-stable"
    chromedriver_path = "/usr/local/bin/chromedriver"
    options = Options()
    options.binary_location = chrome_path
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    #options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-insecure-localhost')

    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # URL corrigida - categoria "Livros" (SCat=2!1) ou "Todos" (SCat=0!1)
    url = f"https://www.fnac.pt/SearchResult/ResultList.aspx?SCat=0!1&Search={query.replace(' ', '+')}"
    print("Abrindo URL:", url)

    driver.get(url)
    time.sleep(5)  # espera carregar a página completamente

    articles = driver.find_elements(By.CSS_SELECTOR, "article.Article-itemGroup")
    print(f"Número de artigos encontrados: {len(articles)}")

    try:
        title_elem = articles[0].find_element(By.CSS_SELECTOR, "a.js-Search-hashLink")
        title = title_elem.text
        print(f"Item {0} título: {title}")
    except Exception as e:
        print(f"Erro no item 0: {e}")

    driver.quit()


if __name__ == "__main__":
    search_fnac("filha da louca")
