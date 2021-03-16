from datetime import datetime

from aiogram.types import Message

from tgbot.config import load_config
from tgbot.services.repository import Repo

config = load_config("bot.ini")
events_chat = config.tg_bot.events_group
now = datetime.now()


# customers
async def new_customer(m: Message, customer_data, customer_id: int):
    event_message = f"""<b>Зарегистрирован аккаунт заказчика №{customer_id}</b>

<b>👨‍💻 Данные аккаунта:</b>
Тип: <code>{customer_data['type']}</code>
Лицо: <code>{customer_data['name']}</code>
Адрес: <code>{customer_data['address']}</code>
Номер телефона: {customer_data['number']}

<i>Дата: {now.hour}:{now.minute} {now.day}.{now.month}.{now.year}</i>"""

    await m.bot.send_message(chat_id=events_chat,
                             text=event_message)


async def customer_changed_profile_data(m: Message, customer_id: int, customer_state_data, repo: Repo):
    customer_db_data = await repo.get_user(user_id=customer_id)
    if customer_state_data['choice'] == "name":
        changed_type = "Лицо"
    elif customer_state_data['choice'] == "address":
        changed_type = "Адрес"
    else:
        changed_type = "Номер телефона"
    event_message = f"""<b>Заказчик №{customer_db_data['id']} сменил личные данные</b>

Тип данных: {changed_type}
Изменение: 
<b>{customer_db_data[customer_state_data['choice']]}</b> → <b>{customer_state_data['new_info']}</b>

<i>Дата: {now.hour}:{now.minute} {now.day}.{now.month}.{now.year}</i>"""

    await m.bot.send_message(chat_id=events_chat,
                             text=event_message)


async def customer_delete_profile(m: Message, customer_data):
    event_message = f"""<b>Заказчик №{customer_data['id']} удален.</b>

<b>👨‍💻 Данные аккаунта:</b>
Лицо: <i>{customer_data['name']}</i>
Адрес: <i>{customer_data['address']}</i>
Номер: {customer_data['number']}

<i>Дата: {now.hour}:{now.minute} {now.day}.{now.month}.{now.year}</i>"""

    await m.bot.send_message(chat_id=events_chat,
                             text=event_message)


# courier
async def new_courier(m: Message, courier_data):
    event_message = f"""<b>Курьер №{courier_data['id']} зарегистрирован</b>

<b>👨‍💻 Данные аккаунта:</b>
Имя: {courier_data['name']}
Номер телефона: {courier_data['number']}

<i>Дата: {now.hour}:{now.minute} {now.day}.{now.month}.{now.year}</i>"""

    await m.bot.send_message(chat_id=events_chat,
                             text=event_message)


async def courier_delete_profile(m: Message, courier_data):
    pass
