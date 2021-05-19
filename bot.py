import asyncio
import logging

import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram_dialog import DialogRegistry
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.config import load_config
from tgbot.filters.role import RoleFilter, AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.admin.broadcast import broadcast
from tgbot.handlers.courier import register_courier
from tgbot.handlers.customer import register_customer
from tgbot.handlers.groups import register_group
from tgbot.handlers.manager import register_manager
from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.role import RoleMiddleware
from tgbot.middlewares.support import SupportMiddleware
from tgbot.middlewares.throttling import ThrottlingMiddleware
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
    logging.getLogger("aiogram_dialog").setLevel(logging.DEBUG)
    logger.info("Starting bot")
    config = load_config("bot.ini")

    if config.tg_bot.use_redis:
        storage = RedisStorage2()
    else:
        storage = MemoryStorage()
    pool = await create_pool(
        user=config.db.user,
        password=config.db.password,
        database=config.db.database,
        host=config.db.host
    )

    bot = Bot(token=config.tg_bot.token, parse_mode='html')
    dp = Dispatcher(bot, storage=storage)

    # aiogram_dialog
    logging.getLogger("aiogram_dialog").setLevel(logging.DEBUG)

    registry = DialogRegistry(dp)
    registry.register(broadcast)

    dp.middleware.setup(ThrottlingMiddleware(limit=.5))
    dp.middleware.setup(DbMiddleware(pool))
    dp.middleware.setup(RoleMiddleware())
    dp.middleware.setup(SupportMiddleware(Dispatcher=dp))
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)

    register_admin(dp)
    register_manager(dp)
    register_courier(dp)
    register_customer(dp)
    register_group(dp)

    # register apscheduler @TODO запустить статистику
    # scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    # scheduler.start()

    # scheduler.add_job(send_stats, 'cron', args=(bot, True, repository.Repo(pool)), hour=23, minute=0,
    #                   replace_existing=True)  # Day stats
    # scheduler.add_job(send_stats, 'cron', args=(bot, True, repository.Repo(pool)), day_of_week='Sun', hour=23, minute=0,
    #                   replace_existing=True)  # week stats

    # start
    try:
        await dp.start_polling()
    finally:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(main())
