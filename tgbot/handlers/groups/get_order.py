from aiogram.types import Message
from tgbot.handlers.admin.order_interaction import generate_order_data_message

from tgbot.services.repository import Repo


async def get_order(m: Message, repo: Repo):
    args = m.get_args()
    if len(args) > 0:
        try:
            answer_message = await generate_order_data_message(order_id=int(args), repo=repo, is_new=False)
            await m.reply(text=answer_message, parse_mode='Markdown')
        except TypeError:
            await m.reply("*🔎 Заказа с таким номером не существует.*",
                          parse_mode='Markdown')
    else:
        answer_message = """Вводите команду /заказ в следующем формате:
/заказ 41
где 41 - номер заказа."""
        await m.reply(text=answer_message, parse_mode='Markdown')
