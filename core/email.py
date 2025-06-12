# /core/email.py
from email.message import EmailMessage
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_price_alert(to_email: str, book_title: str, old_price: float, new_price: float, store: str, link: str):
    msg = EmailMessage()
    msg["Subject"] = f"📉 Baixa de preço: {book_title} na {store}"
    msg["From"] = f"BookHunter <{EMAIL_ADDRESS}>"
    msg["To"] = to_email

    msg.set_content(f"""
Olá!

O livro "{book_title}" baixou de preço na loja {store}!

Preço anterior: {old_price:.2f}€
Preço atual: {new_price:.2f}€

Veja o link: {link}

Boas leituras! 📚
-- Equipa BookHunter
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        
        smtp.send_message(msg)

from email.mime.text import MIMEText

async def send_reset_email(email: str, reset_link: str):
    
    html = f"""
    <html>
    <body>
        <p>Olá,</p>
        <p>Clica no link abaixo para repor a tua palavra-passe:</p>
        <p><a href="{reset_link}">Repor palavra-passe</a></p>
        <p>Se não pediste isto, ignora este email.</p>
    </body>
    </html>
    """

    msg = MIMEText(html, "html")
    msg["From"] = f"BookHunter <{EMAIL_ADDRESS}>"
    msg["To"] = email
    msg["Subject"] = "Reposição da tua palavra-passe"

    # Usa Gmail, por exemplo
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

from itsdangerous import URLSafeTimedSerializer, BadSignature

SECRET_KEY = "mysupersecretkey"
SALT = "reset-senha"
serializer = URLSafeTimedSerializer(SECRET_KEY)

def generate_reset_token(email: str) -> str:
    return serializer.dumps(email, salt=SALT)

def verify_reset_token(token: str, max_age=3600) -> str | None:
    try:
        return serializer.loads(token, salt=SALT, max_age=max_age)
    except BadSignature:
        return None