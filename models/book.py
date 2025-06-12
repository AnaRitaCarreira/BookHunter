# models/book.py
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    url: Mapped[str]
    current_price: Mapped[float]
    lowest_price: Mapped[float]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
