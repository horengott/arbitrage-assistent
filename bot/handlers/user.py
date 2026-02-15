import asyncio
from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.states import Simulation

from db.database import async_session
from db.crud import save_user_history

import keyboards.keyboards as kb

from exchange.fetcher import get_arbitrage_analysis


router = Router()


# starting, selecting trading mode:

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    us_name = message.from_user.first_name
    us_id = message.from_user.id
    await message.answer(f"""{message.from_user.first_name}, welcome to Arbitrage Assistent Bot! 🚀\n
I am your professional assistant for finding and executing profitable cryptocurrency arbitrage deals between top global exchanges. I monitor prices, calculate network fees, and analyze order books in real-time to find the best spreads for you.
\nChoose your mode to get started:""", reply_markup=kb.start_kb)


# simulation mode:

@router.callback_query(F.data == "simulation")
async def deposit_sim_funds(callback: CallbackQuery, state: FSMContext):
    await state.update_data(mode="simulation")
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
   symbol = token.split('/')[0]

   user_data = await state.get_data()
   amount = float(user_data.get('balance', 100))
   mode = user_data.get('mode', 'simulation')

   waiting_sticker = await callback.message.answer_sticker("CAACAgIAAxkBAAEQc41phy81g-W0BctoTROfJwsDDMZcbQACIwADKA9qFCdRJeeMIKQGOgQ")
   loading_msg = await callback.message.answer(f"analyzing {symbol} for {amount} USDT...")
   
   try:
        async with async_session() as session:
            await save_user_history(
                session=session,
                telegram_id=callback.from_user.id,
                username=callback.from_user.username,
                first_name=callback.from_user.first_name,
                mode=mode,
                amount=amount,
                token=symbol
            )
   except Exception as e:
        print(f"⚠️ failed db: {e}")

   result = await get_arbitrage_analysis(symbol, amount)

   await waiting_sticker.delete()

   if result["found"]:
        analysis = result['analysis']
        
        text = (
            f"🔵 **Buy:** {result['buy_exchange'].title()} (${result['buy_price']})\n"
            f"🟠 **Sell:** {result['sell_exchange'].title()} (${result['sell_price']})\n"
            f"────────────────\n"
            f"💰 **Net Profit:** {analysis['profit_pct']}% \n"
            f"💵 **Profit (USD):** ${analysis['profit_usd']}\n"
            f"📉 *Network Fees: ${analysis['withdraw_fee_paid']}*"
        )
        
        await loading_msg.edit_text(text)

   else:
       await loading_msg.edit_text(f"⚠️ No profitable routes found for {symbol}")


# real trading mode:

@router.callback_query(F.data == "real_mode")
async def initializing_real_mode(callback: CallbackQuery):
    await callback.message.answer("📊 Real Trading Mode \n Select exchanges, log in and start trading:", reply_markup=kb.get_list_exchanges(page=0))


@router.callback_query(F.data.startswith("page-"))
async def change_kb_exchanges_page(callback: CallbackQuery):
    page_num = int(callback.data.split("-")[1])
    await callback.message.edit_text("Choose exchanges to log in:", reply_markup=kb.get_list_exchanges(page=page_num))
    await callback.answer()