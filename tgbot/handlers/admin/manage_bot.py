from aiogram.types import Message

from tgbot.keyboards.default.admin.manage_bot import manage_bot_kb
from tgbot.services import Repo


async def manage_bot(m: Message, repo: Repo):
    person_data = await repo.get_partner(admin_id=m.chat.id)
    await m.reply(text="Меню управления ботом:",
                  reply_markup=await manage_bot_kb(is_main=person_data['ismain']))
