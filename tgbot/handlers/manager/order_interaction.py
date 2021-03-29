from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

from tgbot.config import load_config
from tgbot.keyboards.inline.courier.order import courier_order_keyboard_kb
from tgbot.keyboards.inline.manager.choose_courier import get_couriers_keyboard
from tgbot.keyboards.inline.manager.order import order_keyboard
from tgbot.keyboards.inline.manager.order_status import change_order_status
from tgbot.services.repository import Repo


async def generate_order_data_message(order_data, courier_data=None, is_new: bool = True):
    order_message = ""
    customer_type = order_data['customertype']
    if is_new and customer_type == "Компания":
        order_message += f"🚩 Новый заказ №{order_data['orderid']} | <b>Компания</b>\n"
    elif is_new and customer_type == "Частное лицо":
        order_message += f"🚩 Новый заказ №{order_data['orderid']} | <b>Частное лицо</b>\n"
    elif is_new is False and customer_type == "Компания":
        order_message += f"🚩 Заказ №{order_data['orderid']} | <b>Компания</b>\n"
    else:
        order_message += f"🚩 Заказ №{order_data['orderid']} | <b>Частное лицо</b>\n"

    order_message += f"🏙️ Город: <code>{order_data['city'].title()}</code>\n"
    order_message += f"⏳ Статус: <code>{order_data['status']}</code>\n"

    if courier_data is None:
        order_message += f"🚚 Курьер: <i>Не выбран</i>\n"
    else:
        order_message += f"🚚 Курьер: №{courier_data['id']} | <i>{courier_data['name']}</i>\n"

    order_message += f"""
📤 Отправитель:
Лицо: <code>{order_data['customername']}</code>
Адрес: <code>{order_data['customeraddress']}</code>
Номер телефона: {order_data['customernumber']}

📥 Получатель:
ФИО: <code>{order_data['ordername']}</code>
Адрес: <code>{order_data['orderaddress']}</code>
Номер телефона: {order_data['ordernumber']}

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
        order_data = await repo.get_order(order_id=order_id)
        courier_id = order_data['courierid']
        if call.message.chat.id not in couriers_list:
            await call.message.edit_text(text=await generate_order_data_message(order_data=order_data,
                                                                                courier_data=await repo.get_courier(
                                                                                    courier_id) if courier_id is not None else None,
                                                                                is_new=False),
                                         reply_markup=await order_keyboard(order_id=order_id))
        else:
            await call.message.edit_text(text=await generate_order_data_message(order_data=order_data,
                                                                                courier_data=await repo.get_courier(
                                                                                    courier_id) if courier_id is not None else None,
                                                                                is_new=False),
                                         reply_markup=await courier_order_keyboard_kb(order_id=order_id))

    else:
        config = load_config("bot.ini")
        await repo.change_order_status(order_id=order_id, order_status=order_status)
        order_data = await repo.get_order(order_id=order_id)
        courier_id = order_data['courierid']
        if call.message.chat.id not in couriers_list:
            await call.message.edit_text(text=await generate_order_data_message(order_data=order_data,
                                                                                courier_data=await repo.get_courier(
                                                                                    courier_id) if courier_id is not None else None,
                                                                                is_new=False),
                                         reply_markup=await order_keyboard(order_id=order_id))
        else:
            await call.message.edit_text(text=await generate_order_data_message(order_data=order_data,
                                                                                courier_data=await repo.get_courier(
                                                                                    courier_id) if courier_id is not None else None,
                                                                                is_new=False),
                                         reply_markup=await courier_order_keyboard_kb(order_id=order_id))
        await call.bot.send_message(chat_id=order_data['customerid'],
                                    text=f"🚩 Статус заказа №{order_id} обновлен!\n"
                                         f"⏳ Статус: <i>{order_data['status']}</i>")
        city_data = await repo.get_partner(city=order_data['city'])
        await call.bot.send_message(chat_id=city_data['ordersgroupid'],
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
    order_id = callback_data['order_id']
    order = await repo.get_order(order_id=order_id)
    available_couriers = await repo.get_available_couriers_list(city=order['city'])
    await call.message.edit_reply_markup(
        reply_markup=await get_couriers_keyboard(array=available_couriers, order_id=callback_data['order_id']))
    await call.answer()


async def set_order_courier(call: CallbackQuery, callback_data: dict, repo: Repo):
    order_id = callback_data['order_id']
    order_data = await repo.get_order(order_id=order_id)
    courier_id = order_data['courierid']

    couriers_list = [courier['userid'] for courier in await repo.get_couriers_list()]
    if callback_data['courier_id'] == "Вернуться":
        if call.message.chat.id not in couriers_list:
            await call.message.edit_text(text=await generate_order_data_message(order_data=order_data,
                                                                                courier_data=await repo.get_courier(
                                                                                    courier_id) if courier_id is not None else None,
                                                                                is_new=False),
                                         reply_markup=await order_keyboard(order_id=order_id))
        else:
            await call.message.edit_text(text=await generate_order_data_message(order_data=order_data,
                                                                                courier_data=await repo.get_courier(
                                                                                    courier_id) if courier_id is not None else None,
                                                                                is_new=False),
                                         reply_markup=await courier_order_keyboard_kb(order_id=order_id))

    else:
        choosed_courier_id = callback_data['courier_id']
        courier_data = await repo.get_courier(courier_id=choosed_courier_id)
        await repo.change_order_courier(order_id=order_id, courier_id=choosed_courier_id)
        if call.message.chat.id not in couriers_list:
            await call.message.edit_text(text=await generate_order_data_message(order_data=order_data,
                                                                                courier_data=await repo.get_courier(
                                                                                    courier_id) if courier_id is not None else None,
                                                                                is_new=False),
                                         reply_markup=await order_keyboard(order_id=order_id))
        else:
            await call.message.edit_text(text=await generate_order_data_message(order_data=order_data,
                                                                                courier_data=await repo.get_courier(
                                                                                    courier_id) if courier_id is not None else None,
                                                                                is_new=False),
                                         reply_markup=await courier_order_keyboard_kb(order_id=order_id))

        await call.bot.send_message(chat_id=choosed_courier_id,
                                    text=await generate_order_data_message(order_data=order_data,
                                                                           courier_data=await repo.get_courier(
                                                                               courier_id) if courier_id is not None else None,
                                                                           is_new=False),
                                    reply_markup=await courier_order_keyboard_kb(order_id=order_id))
        await call.message.answer(
            text=f"🚩 Курьер заказа №{order_id} изменен!\n🚚 Курьер: №{courier_data['id']} {courier_data['name']}")
        await call.answer(text=f"Заказ {courier_data['name']} назначен на выполнение заказа",
                          show_alert=True)
    await call.answer()


async def current_page_error(call: CallbackQuery):
    await call.answer(cache_time=60)


# Update order
async def update_order_info(call: CallbackQuery, callback_data: dict, repo: Repo):
    order_id = callback_data['order_id']
    order_data = await repo.get_order(order_id=order_id)
    courier_id = order_data['courierid']
    try:
        couriers_list = [courier['userid'] for courier in await repo.get_couriers_list()]
        if call.message.chat.id not in couriers_list:
            await call.message.edit_text(text=await generate_order_data_message(order_data=order_data,
                                                                                courier_data=await repo.get_courier(
                                                                                    courier_id) if courier_id is not None else None,
                                                                                is_new=False),
                                         reply_markup=await order_keyboard(order_id=order_id))
        else:
            await call.message.edit_text(text=await generate_order_data_message(order_data=order_data,
                                                                                courier_data=await repo.get_courier(
                                                                                    courier_id) if courier_id is not None else None,
                                                                                is_new=False),
                                         reply_markup=await courier_order_keyboard_kb(order_id=order_id))

        await call.answer(text=f"Заказ №{order_id} обновлен.")
    except MessageNotModified:
        await call.answer(text=f"Нет изменений в заказе №{order_id}.")
