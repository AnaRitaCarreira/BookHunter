from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="./templates")


@router.get("/index.html", response_class=HTMLResponse)
async def index_page():
    with open("./templates/index.html", encoding="utf-8") as f:
        return f.read()

@router.get("/contacts.html", response_class=HTMLResponse)
async def contacts_page():
    with open("./templates/contacts.html", encoding="utf-8") as f:
        return f.read()

@router.get("/index_ebooks.html", response_class=HTMLResponse)
async def ebooks_page():
    with open("./templates/index_ebooks.html", encoding="utf-8") as f:
        return f.read()

@router.get("/login.html", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
    
@router.get("/sign_up.html", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("sign_up.html", {"request": request})
    # 
    # return templates.TemplateResponse("/login.html", {"request": request})

@router.get("/repor_password.html", response_class=HTMLResponse)
async def repor_password_page(request: Request):
    return templates.TemplateResponse("repor_password.html", {"request": request})
    # 
    
@router.get("/reset_password.html", response_class=HTMLResponse)
async def reset_password_page(request: Request):
    return templates.TemplateResponse("reset_password.html", {"request": request})
    # 


@router.get("/", response_class=HTMLResponse)

async def root():
    with open("./templates/index.html", encoding="utf-8") as f:
        return f.read()
