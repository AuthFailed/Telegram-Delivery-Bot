from aiogram.types import Message

from tgbot.handlers.manager.order_interaction import generate_order_data_message
from tgbot.keyboards.inline.manager.order import order_keyboard
from tgbot.services.repository import Repo


async def get_order(m: Message, repo: Repo):
    args = m.get_args()
    if len(args) > 0:
        try:
            order_data = await repo.get_order(order_id=int(args))
            courier_id = order_data['courierid']
            answer_message = await generate_order_data_message(order_data=order_data, courier_data=await repo.get_courier(
                courier_id) if courier_id is not None else None if courier_id is not None else None if courier_id is not None else None if courier_id is not None else None if courier_id is not None else None, is_new=False)
            await m.reply(text=answer_message,
                          reply_markup=await order_keyboard(order_id=order_data['orderid']))
        except TypeError:
            await m.reply("<b>🔎 Заказа с таким номером не существует.</b>")
    else:
        answer_message = """Вводите команду /заказ в следующем формате:
<code>/заказ 41</code>
где 41 - номер заказа."""
        await m.reply(text=answer_message)
