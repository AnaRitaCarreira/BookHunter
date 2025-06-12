BookHunter/
│
├── scrapers/               # Web scrapers (já tens)
│   └── *.py
├── services/               # Lógica central de agregação
│   └── aggregator.py
├── core/                   # Configurações, email, autenticação
│   ├── config.py
│   └── email.py
├── models/                 # Modelos do ORM (SQLModel, pydantic ou similar)
│   └── user.py, book.py, tbr.py
├── db/                     # DB setup e repositórios
│   └── database.py
├── tasks/                  # Tarefas em background (Celery ou FastAPI BackgroundTasks)
│   └── price_tracker.py
├── api/
│   ├── routes/
│   │   ├── search.py       # 🔍 Pública
│   │   ├── tbr.py          # 📚 Privada (user auth)
│   │   └── auth.py         # 🔐 Login, register
├── main.py                 # Criação do FastAPI app
