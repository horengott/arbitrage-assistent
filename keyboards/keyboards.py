from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# asking trading mode (real o simulation):

start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Real trading 💰", callback_data="real_mode")], [InlineKeyboardButton(text="Simulation 📊", callback_data="simulation")]
])


# token pagination:

TOP_TOKENS = [
"BIC", "ETH", "USDT", "BNB",
"SOL", "XRP", "USDC", "ARB", "TON", 
"DOGE", "DOT", "TRX", "LINK", "MATIC",
"WBTC", "SUI", "LTC", "BONK", "ВСН", "SHIB",
"ADA", "AVAX", "UNI", "DAI", "ATOM"
]

def get_top_tokens(page=0):
    builder = InlineKeyboardBuilder()

    tokens_per_page = 10
    start = tokens_per_page * page
    end = start + tokens_per_page
    current_tokens = TOP_TOKENS[start:end]

    for token in current_tokens:
        builder.button(text=f"{token} 💎", callback_data=f"{token}/USDT")

    builder.adjust(3)

    navigation_btns = []

    if page > 0:
        navigation_btns.append(InlineKeyboardButton(text="⬅️", callback_data=f"page_{page -1 }"))
    
    if end < len(TOP_TOKENS):
        navigation_btns.append(InlineKeyboardButton(text="➡️", callback_data=f"page_{page + 1}"))

    if navigation_btns:
        builder.row(*navigation_btns)

    return builder.as_markup()