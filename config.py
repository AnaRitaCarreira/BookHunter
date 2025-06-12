
import os
from dotenv import load_dotenv

load_dotenv()

# Lê a variável do .env ou usa default (com driver assíncrono aiosqlite)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./db.sqlite3")

# Outras configs
SECRET_KEY = os.getenv("SECRET_KEY", "supersupersecretkeyy_")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")