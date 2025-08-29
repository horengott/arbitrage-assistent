import asyncio
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from states.states import Registration

import keyboards.keyboards as kb

from models.models import User


user = User()


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user.name = message.from_user.first_name
    user.id = message.from_user.id
    await state.set_state(Registration.arbitrage_mode)
    await message.answer(f"hey {message.from_user.first_name}, its your arbitrage assistent. select your mode:", reply_markup=kb.select_mode)


@router.message(F.text == "simulation")
async def user_simulation(message: Message, state: FSMContext):
    user.simulation = True
    await state.update_data(arbitrage_mode=message.text)
    await state.set_state(Registration.balance)
    await message.answer("how much usdt?", reply_markup=ReplyKeyboardRemove())


@router.message(Registration.balance)
async def select_first_token(message: Message, state: FSMContext):
    user.balance = float(message.text)
    await state.update_data(balance=message.text)
    await state.set_state(Registration.currency_1)
    await message.answer("choose a token:")
    await message.answer(f"{user.name}, {user.id}, {user.simulation}, {user.balance}")



