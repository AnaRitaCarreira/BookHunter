from pydantic import BaseModel
from typing import Optional
from pydantic import  EmailStr
from fastapi_users import schemas

class BookCreate(BaseModel):
    title: str
    author: Optional[str]
    cover: Optional[str]
    price: Optional[float]
    store: Optional[str]
    store_url: Optional[str]
    isbn:Optional[str]
    user_email:Optional[str]
    is_ebook:Optional[bool]

class UserRead(schemas.BaseUser[int]):
    id: int
    name: str
    email: EmailStr

class UserCreate(schemas.BaseUserCreate):
    name: str
    email: EmailStr
    password: str

class UserUpdate(schemas.BaseUserUpdate):
    pass
