import asyncio
from aiogram import F, Router
from aiogram.filters import Command

from db.crud import get_users_last_week

router = Router()