from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


select_mode = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="real arbitrage"), KeyboardButton(text="simulation")]], 
    resize_keyboard=True, input_field_placeholder="select mode")