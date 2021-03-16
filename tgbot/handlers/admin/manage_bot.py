from aiogram.types import Message

from tgbot.keyboards.default.admin.manage_bot import keyboard


async def manage_bot(m: Message):
    await m.reply(text="Меню управления ботом:",
                  reply_markup=keyboard)
