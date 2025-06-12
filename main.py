from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from base import Base
from database import engine
from scheduler import start_scheduler

from api.routes import (
    user_dashboard,
    search,
    pages,         # <-- Aqui estão suas rotas HTML (login, index, etc)
    tracking,
    auth_routes    # Rota customizada, se tiver algo além do fastapi-users
)

from auth_funcs import fastapi_users, auth_backend
from schemas import UserCreate, UserRead, UserUpdate
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse

class RedirectUnauthorizedMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if response.status_code == 401 and request.url.path.startswith("/dashboard"):
            return RedirectResponse(url="/login.html")
        return response
    
app = FastAPI()
app.add_middleware(RedirectUnauthorizedMiddleware)

import os
print(">>> Existe o Chrome em /usr/bin/google-chrome-stable?", os.path.exists("/usr/bin/google-chrome-stable"))
print(">>> Conteúdo de /usr/bin:")
print(os.listdir("/usr/bin")[:50])

import shutil
print(">>> `which chrome`: ", shutil.which("chrome"))
print(">>> `which google-chrome-stable`: ", shutil.which("google-chrome-stable"))
print("which chromium:", shutil.which("chromium"))
print("which chromium-browser:", shutil.which("chromium-browser"))

# Servir arquivos estáticos (CSS, JS, imagens)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup inicial: DB e scheduler
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    start_scheduler()

# Rotas "customizadas"
app.include_router(search.router)
app.include_router(pages.router)         # <-- ESSA é a que serve login.html etc
app.include_router(tracking.router)
app.include_router(auth_routes.router)   # se precisar, senão pode remover

# FastAPI Users
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"]
)

# Protegida com autenticação
app.include_router(user_dashboard.router)

app.include_router(tracking.router, prefix="/track")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # coloque a URL do seu frontend aqui
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)