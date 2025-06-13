import tempfile
import shutil
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_isolated_driver():
    chrome_path = os.environ.get("CHROME_BIN", "/usr/bin/google-chrome-stable")
    options = Options()
    options.binary_location = chrome_path
    options.add_argument("--headless=new")  # mais estável nas versões recentes
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

    # Criar diretório temporário exclusivo para o perfil do Chrome
    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={user_data_dir}")

    try:
        service = Service()  # usa o chromedriver do PATH
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(30)  # limite de tempo para evitar travamentos
        return driver, user_data_dir
    except Exception as e:
        shutil.rmtree(user_data_dir, ignore_errors=True)
        raise e
