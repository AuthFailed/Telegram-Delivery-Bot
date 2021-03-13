from aiogram.types import CallbackQuery

from tgbot.keyboards.inline.manager.order import order_keyboard
from tgbot.services.repository import Repo


async def change_order_status_db(call: CallbackQuery, callback_data: dict, repo: Repo):
    await call.answer()
    order_id = int(callback_data.get("order_id"))
    order_status = callback_data.get("status")
    if order_status == "Вернуться":
        order_data_coroutine = await repo.get_order(order_id=order_id)
        order_data = await order_data_coroutine
        order_text = f"""🚩 Новый заказ №{order_id} | *Компания*
⏳ Статус: _{order_data['status']}_

📤 Отправитель:
Название: `{order_data['customername']}`
Адрес: `{order_data['customeraddress']}`
Номер телефона: `{order_data['customernumber']}`

📥 Получатель:
ФИО: `{order_data['ordername']}`
Номер: `{order_data['ordernumber']}`
Адрес: `{order_data['orderaddress']}`

📦 О заказе:
Дата и время доставки: `{order_data['ordertime']}`
Комментарий к заказу: `{order_data['otherdetails']}`"""
        await call.message.edit_text(text=order_text,
                                     reply_markup=await order_keyboard(order_id=order_id),
                                     parse_mode="MARKDOWN")
    else:
        await repo.change_order_status(order_id=order_id, order_status=order_status)
        order_data_coroutine = await repo.get_order(order_id=order_id)
        order_data = await order_data_coroutine

        order_text = f"""🚩 Новый заказ №{order_id} | *Компания*
⏳ Статус: _{order_data['status']}_
    
📤 Отправитель:
Название: `{order_data['customername']}`
Адрес: `{order_data['customeraddress']}`
Номер телефона: `{order_data['customernumber']}`
    
📥 Получатель:
ФИО: `{order_data['ordername']}`
Номер: `{order_data['ordernumber']}`
Адрес: `{order_data['orderaddress']}`
    
📦 О заказе:
Дата и время доставки: `{order_data['ordertime']}`
Комментарий к заказу: `{order_data['otherdetails']}`"""
        await call.message.edit_text(text=order_text,
                                     reply_markup=await order_keyboard(order_id=order_id),
                                     parse_mode="MARKDOWN")

        await call.bot.send_message(chat_id=order_data['customerid'],
                                    text=f"🚩 Статус заказа №{order_id} обновлен!\n"
                                         f"⏳ Статус: _{order_data['status']}_",
                                    parse_mode="MARKDOWN")
