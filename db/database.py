import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import String, ForeignKey, Float, DateTime, func, BigInteger, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')


engine = create_async_engine(f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}', echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


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


async def init_db():
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)
            print("✅ tables created")
        except:
            print("❌ db initiation failed")


async def get_users_last_week(session):
    one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    
    stmt = select(User).where(User.created_at >= one_week_ago)
    
    result = await session.execute(stmt)
    return result.scalars().all()


if __name__ == '__main__':
    asyncio.run(init_db())


