import asyncio
from aiogram import F, Router
from aiogram.filters import Command

from db.database import get_users_last_week

router = Router()