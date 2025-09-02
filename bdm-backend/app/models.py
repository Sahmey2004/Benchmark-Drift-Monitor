
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, Date
from .database import Base

class Price(Base):
    __tablename__ = "prices"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(32), index=True)
    date: Mapped[str] = mapped_column(Date, index=True)
    adj_close: Mapped[float] = mapped_column(Float)
