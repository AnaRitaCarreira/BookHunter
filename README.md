# 📚 Book Finder PT

Um web app que permite pesquisar livros físicos e eBooks em **sites portugueses** como Bertrand, Wook e FNAC, e ainda criar uma lista personalizada de livros "To Be Read" (TBR). O app envia notificações por **email** quando os livros da sua lista ficam **mais baratos**.

---

## ✨ Funcionalidades

- 🔍 **Pesquisa de livros** nos principais sites portugueses (Bertrand, Wook, FNAC)
- ✅ **Registo e login de utilizadores**
- 📋 **Criação de lista TBR** (To Be Read)
- 💸 **Monitorização de preços** e envio de **emails automáticos** quando um livro fica mais barato
- 💾 **Base de dados persistente** para guardar listas por utilizador
- 🧠 Scraping feito com **Selenium** + Chrome headless

---

## 🚀 Tecnologias

- **Python 3.10**
- **FastAPI** (backend)
- **Selenium** (web scraping)
- **SQLite / PostgreSQL** (base de dados)
- **Docker** (deploy containerizado)
- **Render.com** (hosting)
- **SMTP** para envio de emails

---

## 🐳 Como correr localmente com Docker

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/book-finder-pt.git
cd book-finder-pt
```

2. Crie o `.env` com suas variáveis (exemplo: SMTP login, email do app, etc.)

3. Construa e inicie o container:

```bash
docker build -t book-finder .
docker run -p 8000:8000 book-finder
```

4. Acesse em [http://localhost:8000](http://localhost:8000)

---

## 🔐 Variáveis de ambiente `.env` (exemplo)

```env
EMAIL_USER=teu_email@gmail.com
EMAIL_PASS=sua_senha
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SECRET_KEY=uma_chave_aleatoria_para_tokens
```

---

## 🖥️ Endpoints principais (API)

| Método | Rota               | Descrição                          |
|--------|--------------------|------------------------------------|
| GET    | `/search`          | Pesquisa livros                    |
| POST   | `/signup`          | Cria um novo utilizador            |
| POST   | `/login`           | Autentica um utilizador            |
| POST   | `/tbr`             | Adiciona livro à lista TBR         |
| GET    | `/tbr`             | Lista os livros da TBR             |

---

## 📬 Notificações

- O app verifica periodicamente (cron job / scheduler) os preços dos livros salvos.
- Se o preço baixar, o utilizador recebe um **email automático** com link direto para o site mais barato.

---

## 📦 Deploy no Render.com

Para funcionar no Render:

- Use o `Dockerfile` incluído com o Chrome instalado manualmente (via `.deb`).
- Configure o serviço como **Docker** em vez de Python.
- Certifique-se de que o `CMD` inicia a app corretamente (`main.py`).

---

## 🤝 Contribuições

Pull requests são bem-vindos! Se encontrar bugs ou quiser sugerir funcionalidades, abra uma _issue_ 🚀

---

## 📝 Licença

MIT © 2025 — Feito com ☕ e paixão por livros em 🇵🇹
