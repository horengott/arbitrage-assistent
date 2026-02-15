from db.database import User, ArbitrageHistory
from sqlalchemy.ext.asyncio import AsyncSession


# saving to db user activity:

async def save_user_history(session: AsyncSession, telegram_id: int, first_name: str, username: str, mode: str, amount: float, token: str):
    user = await session.get(User, telegram_id)
    if not user:
        user = User(id=telegram_id, username=username, name=first_name, balance_usdt=0.0)
        session.add(user)
        await session.flush() 

    log = ArbitrageHistory(
        user_id = telegram_id,
        mode = mode,
        token_symbol = token.upper(),
        amount_usdt = amount
    )
    
    session.add(log)
    await session.commit()