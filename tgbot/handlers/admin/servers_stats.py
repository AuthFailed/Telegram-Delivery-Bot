from aiogram.types import Message

from tgbot.services.server_stats import stats


async def servers_stats(m: Message):
    await m.answer(text=await stats())
