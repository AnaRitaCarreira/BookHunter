class TBR(Base):
    __tablename__ = "tbr"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    price_alert: Mapped[float] = mapped_column(nullable=True)
