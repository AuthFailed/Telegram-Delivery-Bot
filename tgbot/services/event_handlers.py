from datetime import datetime

from aiogram.types import Message

from tgbot.config import load_config
from tgbot.services.repository import Repo

config = load_config("bot.ini")
events_chat = config.tg_bot.events_group
now = datetime.now()


# customers
async def new_customer(m: Message, customer_data, customer_id: int):
    event_message = f"""*Зарегистрирован аккаунт заказчика №{customer_id}*

*👨‍💻 Данные аккаунта:*
Тип: _{customer_data['type']}_
Лицо: _{customer_data['name']}_
Адрес: _{customer_data['address']}_
Номер телефона: {customer_data['number']}

_Дата: {now.hour}:{now.minute} {now.day}.{now.month}.{now.year}_"""

    await m.bot.send_message(chat_id=events_chat,
                             text=event_message,
                             parse_mode='Markdown')


async def customer_changed_profile_data(m: Message, customer_id: int, customer_state_data, repo: Repo):
    customer_db_data = await repo.get_user(user_id=customer_id)
    if customer_state_data['choice'] == "name":
        changed_type = "Лицо"
    elif customer_state_data['choice'] == "address":
        changed_type = "Адрес"
    else:
        changed_type = "Номер телефона"
    event_message = f"""*Заказчик №{customer_db_data['id']} сменил личные данные*

Тип данных: {changed_type}
Изменение: 
*{customer_db_data[customer_state_data['choice']]}* → *{customer_state_data['new_info']}*

_Дата: {now.hour}:{now.minute} {now.day}.{now.month}.{now.year}_"""

    await m.bot.send_message(chat_id=events_chat,
                             text=event_message,
                             parse_mode='Markdown')


async def customer_delete_profile(m: Message, customer_data):
    event_message = f"""*Заказчик №{customer_data['id']} удален.*

*👨‍💻 Данные аккаунта:*
Лицо: _{customer_data['name']}_
Адрес: _{customer_data['address']}_
Номер: {customer_data['number']}

_Дата: {now.hour}:{now.minute} {now.day}.{now.month}.{now.year}_"""

    await m.bot.send_message(chat_id=events_chat,
                             text=event_message,
                             parse_mode='Markdown')


# courier
async def new_courier(m: Message, courier_data):
    event_message = f"""*Курьер №{courier_data['id']} зарегистрирован*

*👨‍💻 Данные аккаунта:*
Имя: {courier_data['name']}
Номер телефона: {courier_data['number']}

_Дата: {now.hour}:{now.minute} {now.day}.{now.month}.{now.year}_"""

    await m.bot.send_message(chat_id=events_chat,
                             text=event_message,
                             parse_mode='Markdown')


async def courier_delete_profile(m: Message, courier_data):
    pass
