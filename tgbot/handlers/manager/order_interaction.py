from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified
from asyncpg import UndefinedColumnError

from tgbot.config import load_config
from tgbot.keyboards.inline.courier.order import courier_order_keyboard_kb
from tgbot.keyboards.inline.manager.choose_courier import choose_courier_kb
from tgbot.keyboards.inline.manager.order import order_keyboard
from tgbot.keyboards.inline.manager.order_status import change_order_status
from tgbot.services.repository import Repo


async def generate_order_data_message(order_data=None, order_id: int = None, is_new: bool = True,
                                      is_company: bool = False, repo: Repo = None):
    order_message = ""
    if order_data is None:
        order_data = await repo.get_order(order_id=order_id)
    if is_new:
        try:
            if is_company:
                order_message += f"🚩 Новый заказ №{order_data['orderid']} | <b>Компания</b>\n"
            else:
                order_message += f"🚩 Новый заказ №{order_data['orderid']} | <b>Частное лицо</b>\n"
        except TypeError:
            return f"Заказ №{order_id} отсутствует в базе данных."
    else:
        if is_company:
            order_message += f"🚩 Заказ №{order_data['orderid'] if order_data is not None else order_id} | <b>Компания</b>\n"
        else:
            order_message += f"🚩 Заказ №{order_data['orderid'] if order_data is not None else order_id} | <b>Частное лицо</b>\n"

    order_message += f"⏳ Статус: <code>{order_data['status']}</code>\n"

    try:
        courier_data = await repo.get_courier_by_userid(courier_id=order_data['courierid'])
        order_message += f"🚚 Курьер: №{order_data['orderid']} | <i>{courier_data['name']}</i>\n"
    except TypeError:
        order_message += f"🚚 Курьер: <i>Не выбран</i>\n"
    except UndefinedColumnError:
        order_message += f"🚚 Курьер: <i>Не выбран</i>\n"

    order_message += f"""
📤 Отправитель:
Лицо: <code>{order_data['customername']}</code>
Адрес: <code>{order_data['customeraddress']}</code>
Номер телефона: {order_data['customernumber']}

📥 Получатель:
ФИО: <code>{order_data['ordername']}</code>
Номер: <code>{order_data['ordernumber']}</code>
Адрес: {order_data['orderaddress']}

📦 О заказе:
Дата и время доставки: <code>{order_data['ordertime']}</code>
Комментарий к заказу: <code>{order_data['otherdetails']}</code>"""
    return order_message


# change order status
async def change_order_status_kb(call: CallbackQuery, callback_data: dict):
    await call.answer(text="Выберите статус из списка под заказом")
    order_id = callback_data.get("order_id")
    await call.message.edit_reply_markup(reply_markup=await change_order_status(order_id=order_id))


async def change_order_status_db(call: CallbackQuery, callback_data: dict, repo: Repo):
    order_id = int(callback_data.get("order_id"))
    order_status = callback_data.get("status")
    couriers_list = [courier['userid'] for courier in await repo.get_couriers_list()]
    if order_status == "Вернуться":
        if call.message.chat.id not in couriers_list:
            await call.message.edit_text(text=await generate_order_data_message(order_id=order_id, repo=repo),
                                         reply_markup=await order_keyboard(order_id=order_id))
        else:
            await call.message.edit_text(text=await generate_order_data_message(order_id=order_id, repo=repo),
                                         reply_markup=await courier_order_keyboard_kb(order_id=order_id))

    else:
        config = load_config("bot.ini")
        await repo.change_order_status(order_id=order_id, order_status=order_status)
        order_data = await repo.get_order(order_id=order_id)

        await call.message.edit_text(text=await generate_order_data_message(order_id=order_id, repo=repo),
                                     reply_markup=await order_keyboard(order_id=order_id))

        await call.bot.send_message(chat_id=order_data['customerid'],
                                    text=f"🚩 Статус заказа №{order_id} обновлен!\n"
                                         f"⏳ Статус: <i>{order_data['status']}/<i>", )
        await call.bot.send_message(chat_id=config.tg_bot.orders_group,
                                    text=f"🚩 Статус заказа №{order_id} обновлен!\n"
                                         f"⏳ Статус: <i>{order_data['status']}</i>")
        if order_data['courierid'] is not None and call.message.chat.id not in couriers_list:
            await call.bot.send_message(chat_id=order_data['courierid'],
                                        text=f"🚩 Статус заказа №{order_id} обновлен!\n"
                                             f"⏳ Статус: <i>{order_data['status']}</i>")
        await call.answer(f"Статус заказа №{order_id} изменен на {order_status}")


# change order courier
async def list_of_available_couriers(call: CallbackQuery, callback_data: dict, repo: Repo):
    await call.answer(text="Выберите курьера из выпадающего списка")
    available_couriers = await repo.get_available_couriers_list()
    await call.message.edit_reply_markup(
        reply_markup=await choose_courier_kb(order_id=callback_data['order_id'], courier_list=available_couriers))
    await call.answer()


async def set_order_courier(call: CallbackQuery, callback_data: dict, repo: Repo):
    order_id = callback_data['order_id']
    couriers_list = [courier['userid'] for courier in await repo.get_couriers_list()]
    if callback_data['courier_id'] == "Вернуться":
        if call.message.chat.id not in couriers_list:
            await call.message.edit_text(text=await generate_order_data_message(order_id=order_id, repo=repo),
                                         reply_markup=await order_keyboard(order_id=order_id))
        else:
            await call.message.edit_text(text=await generate_order_data_message(order_id=order_id, repo=repo),
                                         reply_markup=await courier_order_keyboard_kb(order_id=order_id))

    else:
        choosed_courier_id = callback_data['courier_id']
        await repo.change_order_courier(order_id=order_id, courier_id=choosed_courier_id)
        if call.message.chat.id not in couriers_list:
            await call.message.edit_text(text=await generate_order_data_message(order_id=order_id, repo=repo),
                                         reply_markup=await order_keyboard(order_id=order_id))
        else:
            await call.message.edit_text(text=await generate_order_data_message(order_id=order_id, repo=repo),
                                         reply_markup=await courier_order_keyboard_kb(order_id=order_id))

        await call.bot.send_message(chat_id=choosed_courier_id,
                                    text=await generate_order_data_message(order_id=order_id, repo=repo),
                                    reply_markup=await courier_order_keyboard_kb(order_id=order_id))
        await call.answer(text=f"Курьер id{choosed_courier_id} назначен на выполнение заказа")
    await call.answer()


# Update order
async def update_order_info(call: CallbackQuery, callback_data: dict, repo: Repo):
    order_id = callback_data['order_id']

    try:
        couriers_list = [courier['userid'] for courier in await repo.get_couriers_list()]
        if call.message.chat.id not in couriers_list:
            await call.message.edit_text(text=await generate_order_data_message(order_id=order_id, repo=repo),
                                         reply_markup=await order_keyboard(order_id=order_id))
        else:
            await call.message.edit_text(text=await generate_order_data_message(order_id=order_id, repo=repo),
                                         reply_markup=await courier_order_keyboard_kb(order_id=order_id))

        await call.answer(text=f"Заказ №{order_id} обновлен.")
    except MessageNotModified:
        await call.answer(text=f"Нет изменений в заказе №{order_id}.")
