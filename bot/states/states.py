from aiogram.fsm.state import StatesGroup, State

class Simulation(StatesGroup):
    mode = State()
    balance = State()
    choose_token = State()
    