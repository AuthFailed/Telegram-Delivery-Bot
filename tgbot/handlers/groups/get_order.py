from aiogram.types import Message

from tgbot.handlers.manager.order_interaction import generate_order_data_message
from tgbot.services.repository import Repo


async def get_order(m: Message, repo: Repo):
    args = m.get_args()
    if len(args) > 0:
        try:
            answer_message = await generate_order_data_message(order_id=int(args), repo=repo, is_new=False)
            await m.reply(text=answer_message)
        except TypeError:
            await m.reply("<b>🔎 Заказа с таким номером не существует.</b>")
    else:
        answer_message = """Вводите команду /заказ в следующем формате:
<code>/заказ 41</code>
где 41 - номер заказа."""
        await m.reply(text=answer_message)
