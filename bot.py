from handlers.admin import admin_statistic
# from handlers.client import client_referal, client_yurist
from handlers import starthandler
from database.base import Base
from database.Database import Database
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from middleware.DatabaseMiddleware import DatabaseMiddleware
from config import bot, dp, base_aunt
import asyncio
import logging
import asyncpg

async def main():
    logging.basicConfig(level=logging.INFO)

    engine = create_async_engine(base_aunt, future=True, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session = async_sessionmaker(engine, expire_on_commit=False).begin().async_session
    database = Database(session=session)

    dp.update.outer_middleware(DatabaseMiddleware(database=database))

    dp.include_router(router=starthandler.router)
    dp.include_router(router=admin_statistic.router)

    try:
        await dp.start_polling(bot)
    finally:
        await session.close()
        await engine.dispose()

if __name__ == '__main__':
    asyncio.run(main())