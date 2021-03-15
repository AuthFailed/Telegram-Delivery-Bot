import asyncio
import logging

import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.config import load_config
from tgbot.filters.role import RoleFilter, AdminFilter
from tgbot.handlers.courier import register_courier
from tgbot.handlers.customer import register_customer
from tgbot.handlers.groups import register_group
from tgbot.handlers.manager import register_manager
from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.role import RoleMiddleware
from tgbot.services import repository
from tgbot.services.stats_sender import send_stats

logger = logging.getLogger(__name__)


async def create_pool(user, password, database, host):
    pool = await asyncpg.create_pool(user=user, password=password, database=database, host=host)
    return pool


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")
    config = load_config("bot.ini")

    if config.tg_bot.use_redis:
        storage = RedisStorage()
    else:
        storage = MemoryStorage()
    pool = await create_pool(
        user=config.db.user,
        password=config.db.password,
        database=config.db.database,
        host=config.db.host
    )

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=storage)
    dp.middleware.setup(DbMiddleware(pool))
    dp.middleware.setup(RoleMiddleware(admin_id=config.tg_bot.admin_id))
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)

    # register_admin(dp)
    register_manager(dp)
    register_courier(dp)
    register_group(dp)
    register_customer(dp)

    # register apscheduler
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.start()
    # scheduler.add_job(send_stats, 'interval', args=(bot, True, repository.Repo(pool)), seconds=10)
    scheduler.add_job(send_stats, 'cron', args=(bot, True, repository.Repo(pool)), hour=23, minute=0,
                      replace_existing=True)  # Day stats
    scheduler.add_job(send_stats, 'cron', args=(bot, True, repository.Repo(pool)), day_of_week='Sun', hour=23, minute=0,
                      replace_existing=True)  # week stats

    # start
    try:
        await dp.start_polling()
    finally:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(main())
