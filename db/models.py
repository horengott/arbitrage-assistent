from sqlalchemy import BigInteger, String, ForeignKey, Float, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import datetime, timedelta
from db.database import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    username: Mapped[str | None] = mapped_column(String(45), nullable=True) 
    name: Mapped[str] = mapped_column(String(45))
    balance_usdt: Mapped[float]

    exchanges: Mapped[List['Exchange']] = relationship(back_populates='user')

    history: Mapped[list["ArbitrageHistory"]] = relationship(back_populates="user")


class ArbitrageHistory(Base):
    __tablename__ = 'arbitrage_history'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id'))
    mode: Mapped[str] = mapped_column(String(50))   
    token_symbol: Mapped[str] = mapped_column(String(20))
    amount_usdt: Mapped[float] = mapped_column(Float)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped['User'] = relationship(back_populates='history')


class Exchange(Base):
    __tablename__ = 'exchanges'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    api_key: Mapped[str] = mapped_column(String(255))
    secret: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id'))
    
    user: Mapped['User'] = relationship(back_populates='exchanges')