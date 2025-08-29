from aiogram.fsm.state import StatesGroup, State

class Registration(StatesGroup):
    arbitrage_mode = State()
    balance = State()
    currency_1 = State()
    currency_2 = State()