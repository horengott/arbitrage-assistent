import asyncio
from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.states import Simulation

import keyboards.keyboards as kb

from models.models import User


user = User()


router = Router()


# starting, selecting trading mode:

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user.name = message.from_user.first_name
    user.id = message.from_user.id
    await message.answer(f"""{message.from_user.first_name}, welcome to Arbitrage Assistent Bot! 🚀\n
I am your professional assistant for finding and executing profitable cryptocurrency arbitrage deals between top global exchanges. I monitor prices, calculate network fees, and analyze order books in real-time to find the best spreads for you.
\nChoose your mode to get started:""", reply_markup=kb.start_kb)


# simulation mode:

@router.callback_query(F.data == "simulation")
async def deposit_sim_funds(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("""📊 Simulation Mode
\nPractice with virtual balance! Test your strategies and see potential profits based on real-time market data without any risk.
\nSpecify USDT balance for simulation operate:""")
    await state.set_state(Simulation.balance)


@router.message(Simulation.balance)
async def choose_sim_token(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Amount of USDT must be a number")
    else:
        await state.update_data(balance=float(message.text))
        await message.answer("Choose a token:", reply_markup=kb.get_top_tokens(page=0))
        await state.set_state(Simulation.choose_token)


@router.callback_query(F.data.startswith("page_"))
async def change_kb_token_page(callback: CallbackQuery):
    page_num = int(callback.data.split("_")[1])
    await callback.message.edit_text("Choose a token:", reply_markup=kb.get_top_tokens(page=page_num))
    await callback.answer()


@router.callback_query(F.data.endswith("/USDT"))
async def take_token(callback: CallbackQuery, state: FSMContext):
   token = callback.data
   user_data = await state.get_data()
   amount = user_data.get('balance', 100)
   await callback.message.answer('Wait... ⏳')


# real trading mode:

@router.callback_query(F.data == "real_mode")
async def initializing_real_mode(callback: CallbackQuery):
    await callback.message.answer("📊 Real Trading Mode \n Select exchanges, log in and start trading:", reply_markup=kb.get_list_exchanges(page=0))


@router.callback_query(F.data.startswith("page-"))
async def change_kb_exchanges_page(callback: CallbackQuery):
    page_num = int(callback.data.split("-")[1])
    await callback.message.edit_text("Choose exchanges to log in:", reply_markup=kb.get_list_exchanges(page=page_num))
    await callback.answer()