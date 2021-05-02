from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageNotModified

from tgbot.handlers.manager.order_interaction import generate_order_data_message
from tgbot.keyboards.inline.customer.pagination import get_pages_keyboard
from tgbot.services.repository import Repo


async def list_of_available_orders(m: Message, repo: Repo):
    customer_orders = await repo.get_customer_orders(userid=m.chat.id)
    if len(customer_orders) > 0:
        await m.answer(text="Ваши заказы:",
                       reply_markup=await get_pages_keyboard(customer_orders))
    else:
        await m.answer(text="Вы еще не совершили ни одного заказа.")


async def show_chosen_page(c: CallbackQuery, callback_data: dict, repo: Repo):
    customer_orders = await repo.get_customer_orders(userid=c.message.chat.id)
    current_page = int(callback_data.get("page"))

    try:
        await c.message.edit_reply_markup(await get_pages_keyboard(customer_orders, page=current_page))
        await c.answer()
    except MessageNotModified:
        await c.answer(text="Страница не изменена")


async def show_item(c: CallbackQuery, callback_data: dict, repo: Repo):
    await c.answer()
    item_id = callback_data['item_id']

    answer_message = f"Выбран заказ №{item_id}\n\n"

    item = await repo.get_order(order_id=item_id)
    courier_id = item['courierid']
    if courier_id is not None:
        answer_message += await generate_order_data_message(order_data=item,
                                                            courier_data=await repo.get_courier(
                                                                courier_id) if courier_id is not None else None,
                                                            is_new=False)
    else:
        answer_message += await generate_order_data_message(order_data=item,
                                                            is_new=False)
    await c.message.answer(text=answer_message)
