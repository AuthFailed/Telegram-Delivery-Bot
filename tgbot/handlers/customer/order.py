from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from tgbot.handlers.admin.order_interaction import generate_order_data_message

from tgbot.config import load_config
from tgbot.keyboards.default.user.check_order import check_order
from tgbot.keyboards.default.user.choose_time import choose_time
from tgbot.keyboards.default.user.main_menu import main_menu
from tgbot.keyboards.default.user.return_to_menu import return_to_menu
from tgbot.keyboards.inline.customer.aiogramcalendar import create_calendar, process_calendar_selection
from tgbot.keyboards.inline.manager.order import order_keyboard
from tgbot.services.repository import Repo
from tgbot.states.user.order import Order


async def order_starts(m: Message, repo: Repo):
    is_user_exists = await repo.is_user_exists(user_id=m.chat.id)

    if is_user_exists:
        customer_data = await repo.get_user(user_id=m.chat.id)
        if customer_data['usertype'] == "Частное лицо":
            answer_message = "Введите данные в следующем формате:\nФИО\nНомер телефона\nАдрес получателя:"
        else:
            answer_message = "Введите данные в следующем формате:\nФИО\nНомер телефона\nАдрес получателя\nДату и время доставки:"
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
                text=f"⏰ Выберите дату доставки:",
                reply_markup=create_calendar(),
            )
            await Order.order_date.set()
        else:
            await m.answer(text="✖️ Введите текст в указаном формате.")
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
            await m.answer(text="✖️ Введите текст в указаном формате.")


async def order_date(call: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await process_calendar_selection(call, callback_data)
    if selected:
        await call.message.edit_text(text=f"Выбрана дата: {date.strftime('%d.%m.%Y')}")
        await state.update_data(order_date=date.strftime("%d.%m.%Y"))

        await call.message.answer(text="⏰ Выберите время доставки:",
                                  reply_markup=choose_time)

        await Order.order_time.set()


async def order_time(m: Message, state: FSMContext):
    await state.update_data(order_time=m.text)

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
    if 'order_datetime' not in data:
        order_datetime = f"{data['order_time']} {data['order_date']}"
    else:
        order_datetime = data['order_datetime']

    await m.reply(text=f"""🚩 Ваш заказ
⏳ Статус: _Редактируется_    
🚚 Курьер: _Не выбран_

📤 Отправитель:
Лицо: `{customer_data['name']}`
Адрес: `{customer_data['address']}`
Номер телефона: `{customer_data['number']}`

📥 Получатель:
ФИО: `{order_data['order_name']}`
Номер: `{order_data['order_number']}`
Адрес: `{order_data['order_address']}`

📦 О заказе:
Дата и время доставки: `{order_datetime}`
Комментарий к заказу: `{order_data['other_details']}`
""",
                  reply_markup=check_order,
                  parse_mode="Markdown")
    await Order.next()


async def order_user_choice(m: Message, repo: Repo, state=FSMContext):
    if m.text == "👌 Все правильно":
        order_data = await state.get_data()
        customer_data = await repo.get_user(user_id=m.chat.id)
        if 'order_datetime' not in order_data:
            order_datetime = f"{order_data['order_time']} {order_data['order_date']}"
        else:
            order_datetime = order_data['order_datetime']

        order_id = await repo.add_order(
            customer_id=m.chat.id,
            customer_type=customer_data["usertype"],
            customer_name=customer_data["name"],
            customer_address=customer_data["address"],
            customer_number=customer_data["number"],
            order_name=order_data["order_name"],
            order_address=order_data["order_address"],
            order_number=order_data["order_number"],
            order_time=order_datetime,
            other_details=order_data["other_details"],
        )

        order_data = await repo.get_order(order_id=order_id)
        config = load_config("bot.ini")
        await m.bot.send_message(chat_id=config.tg_bot.orders_group,
                                 text=await generate_order_data_message(order_data=order_data, is_new=True,
                                                                        is_company=True if customer_data[
                                                                                               "usertype"] == "Компания" else False,
                                                                        repo=repo),
                                 reply_markup=await order_keyboard(order_id=order_id),
                                 parse_mode="Markdown")

        await m.answer(
            text=f"🚩 Заказ №{order_id} отправлен!\n"
                 f"⏳ Статус: _Обрабатывается_",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="Markdown"
        )
        await state.finish()
        await m.answer(text="Главное меню",
                       reply_markup=await main_menu(reg=True))
    elif m.text == "🔄 Заполнить заново":
        await state.reset_data()
        customer = await repo.get_user(user_id=m.chat.id)
        customer_type = customer['usertype']

        if customer_type == "Частное лицо":
            answer_message = "Введите данные в следующем формате:\nФИО\nНомер телефона\nАдрес получателя:"
        else:
            answer_message = "Введите данные в следующем формате:\nФИО\nНомер телефона\nАдрес получателя\nДату и время доставки:"
        await m.answer(
            text=answer_message,
            reply_markup=return_to_menu,
        )
        await Order.first()
