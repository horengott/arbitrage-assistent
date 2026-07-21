from db.models import User, ArbitrageHistory
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from sqlalchemy import select


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


async def get_users_last_week(session):
    one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    
    stmt = select(User).where(User.created_at >= one_week_ago)
    
    result = await session.execute(stmt)
    return result.scalars().all()