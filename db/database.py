import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List
from dotenv import load_dotenv

load_dotenv()
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')


engine = create_async_engine(f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(45))
    name: Mapped[str] = mapped_column(String(45))
    balance_usdt: Mapped[float]
    exchanges: Mapped[List['Exchange']] = relationship(back_populates='user')


class Exchange(Base):
    __tablename__ = 'exchanges'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    api_key: Mapped[str] = mapped_column(String(255))
    secret: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='exchanges')


async def init_db():
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)
            print("db tables were created")
        except:
            print("an error has produced")


if __name__ == '__main__':
    asyncio.run(init_db())


