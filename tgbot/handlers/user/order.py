from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from tgbot.config import load_config
from tgbot.keyboards.default.user.check_order import check_order
from tgbot.keyboards.default.user.choose_time import choose_time
from tgbot.keyboards.default.user.main_menu import main_menu
from tgbot.keyboards.default.user.return_to_menu import return_to_menu
from tgbot.keyboards.inline.admin.order import order_keyboard
from tgbot.services.repository import Repo
from tgbot.states.user.order import Order


async def order_starts(m: Message, repo: Repo):
    is_user_exists = await repo.is_user_exists(user_id=m.chat.id)

    if is_user_exists:
        customer_data = await repo.get_user(user_id=m.chat.id)
        if customer_data['usertype'] == "Частное лицо":
            answer_message = "Введите:\nФИО\nНомер телефона\nАдрес получателя:"
        else:
            answer_message = "Введите:\nФИО\nНомер телефона\nАдрес получателя\nДату и время доставки:"
        await m.reply(text=answer_message,
                      reply_markup=return_to_menu)
        await Order.first()


async def order_all_info(m: Message, repo: Repo, state: FSMContext):
    customer_data = await repo.get_user(user_id=m.chat.id)
    user_type = customer_data['usertype']
    await state.update_data(user_type=user_type)

    spliced_info = m.text.splitlines()
    if user_type == "Частное лицо":
        if len(spliced_info) == 3:
            order_name = spliced_info[0]
            order_number = spliced_info[1]
            order_address = spliced_info[2]
            await state.update_data(
                order_name=order_name,
                order_number=order_number,
                order_address=order_address,
            )
            await m.answer(
                text=f"⏰ Выберите время доставки:",
                reply_markup=choose_time,
            )
            await Order.order_datetime.set()
        else:
            await m.answer(text="❌ Введите текст в указаном формате.")
    else:
        if len(spliced_info) == 4:
            order_name = spliced_info[0]
            order_number = spliced_info[1]
            order_address = spliced_info[2]
            order_datetime = spliced_info[3]
            await state.update_data(
                order_name=order_name,
                order_number=order_number,
                order_address=order_address,
                order_datetime=order_datetime,
            )
            await m.answer(
                text=f"""Напишите подробное описание того, что нужно купить или что нужно забрать курьеру
Например: 1 литр молока Простоквашино, хлеб 1 буханка круглый и так далее,
так же указать магазин в котором нужно купить (магнит,пятёрочка и т.д)""",
                reply_markup=return_to_menu,
            )
            await Order.other_details.set()
        else:
            await m.answer(text="❌ Введите текст в указаном формате.")


async def order_datetime(m: Message, state: FSMContext):
    time = m.text

    await state.update_data(order_datetime=time)
    await m.answer(
        text=f"""Напишите подробное описание что нужно купить или что нужно забрать курьеру
    Например: 1 литр молока Простоквашино, хлеб 1 буханка круглый и так далее,
    так же указать магазин в котором нужно купить (магнит,пятёрочка и т.д)""",
        reply_markup=return_to_menu)
    await Order.other_details.set()


async def order_other_details(m: Message, repo: Repo, state: FSMContext):
    other_details = m.text
    async with state.proxy() as data:
        data['other_details'] = other_details
        order_data = data
    customer_data = await repo.get_user(user_id=m.chat.id)

    if order_data['user_type'] == "Частное лицо":
        message_to_send = (
            f"""🚩 Ваша заявка
⏳ Статус: _Редактирование_

📤 Отправитель:
ФИО: `{customer_data['name']}`
Адрес: `{customer_data['address']}`
Номер телефона: `{customer_data['number']}`

📥 Получатель:
ФИО: `{order_data['order_name']}`
Адрес: `{order_data['order_address']}`
Номер телефона: `{order_data['order_number']}`

📦 О заказе:
Время доставки: `{order_data['order_datetime']}`
Комментарий к заказу: `{order_data['other_details']}`"""
        )
    else:
        message_to_send = (
            f"""🚩 Ваша заявка!
⏳ Статус: _Редактирование_

📤 Отправитель:
Название: `{customer_data['name']}`
Адрес: `{customer_data['address']}`
Номер телефона: `{customer_data['number']}`

📥 Получатель:
ФИО: `{order_data['order_name']}`
Адрес: `{order_data['order_address']}`
Номер: `{order_data['order_number']}`

📦 О заказе:
Дата и время доставки: `{order_data['order_datetime']}`
Комментарий к заказу: `{order_data['other_details']}`"""
        )
    await m.reply(text=message_to_send,
                  reply_markup=check_order,
                  parse_mode="MARKDOWN")
    await Order.next()


async def order_user_choice(m: Message, repo: Repo, state=FSMContext):
    if m.text == "👌 Все правильно":
        order_data = await state.get_data()
        customer_data = await repo.get_user(user_id=m.chat.id)

        order_id = await repo.add_order(
            customer_id=m.chat.id,
            customer_type=customer_data["usertype"],
            customer_name=customer_data["name"],
            customer_address=customer_data["address"],
            customer_number=customer_data["number"],
            order_name=order_data["order_name"],
            order_address=order_data["order_address"],
            order_number=order_data["order_number"],
            order_time=order_data["order_datetime"],
            other_details=order_data["other_details"],
        )

        if customer_data["usertype"] == "Частное лицо":
            message_to_send = (
                f"""🚩 Новая заявка №{order_id} | *Частное лицо*
⏳ Статус: _Обрабатывается_

📤 Отправитель:
ФИО: `{customer_data['name']}`
Адрес: `{customer_data['address']}`
Номер телефона: `{customer_data['number']}`

📥 Получатель:
ФИО: `{order_data['order_name']}`
Адрес: `{order_data['order_address']}`
Номер телефона: `{order_data['order_number']}`

📦 О заказе:
Время доставки: `{order_data['order_datetime']}`
Комментарий к заказу: `{order_data['other_details']}`"""
            )
        else:
            message_to_send = (
                f"""🚩 Новая заявка №{order_id} | *Компания*
⏳ Статус: _Обрабатывается_

📤 Отправитель:
Название: `{customer_data['name']}`
Адрес: `{customer_data['address']}`
Номер телефона: `{customer_data['number']}`

📥 Получатель:
ФИО: `{order_data['order_name']}`
Номер: `{order_data['order_number']}`
Адрес: `{order_data['order_address']}`

📦 О заказе:
Дата и время доставки: `{order_data['order_datetime']}`
Комментарий к заказу: `{order_data['other_details']}`"""
            )

        config = load_config("bot.ini")
        await m.bot.send_message(chat_id=config.tg_bot.orders_group,
                                 text=message_to_send,
                                 reply_markup=await order_keyboard(order_id=order_id),
                                 parse_mode="MARKDOWN")

        await m.answer(
            text=f"🚩 Заявка №{order_id} отправлена!\n"
                 f"⏳ Статус: _Обрабатывается_",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="MARKDOWN"
        )
        await state.finish()
        await m.answer(text="Главное меню",
                       reply_markup=await main_menu(reg=True))
    elif m.text == "🔄 Заполнить заново":
        await state.reset_data()
        customer = await repo.get_user(user_id=m.chat.id)
        customer_type = customer['usertype']

        if customer_type == "Частное лицо":
            answer_message = "Введите:\nФИО\nНомер телефона\nАдрес получателя:"
        else:
            answer_message = "Введите:\nФИО\nНомер телефона\nАдрес получателя\nДату и время доставки:"
        await m.answer(
            text=answer_message,
            reply_markup=return_to_menu,
        )
        await Order.first()
