from aiogram.fsm.state import StatesGroup, State

class Simulation(StatesGroup):
    balance = State()
    choose_token = State()
    