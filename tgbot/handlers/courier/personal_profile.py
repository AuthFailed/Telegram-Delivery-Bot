from aiogram.types import Message

from tgbot.keyboards.default.courier.personal_profile import personal_profile_kb
from tgbot.services.repository import Repo


async def personal_profile(m: Message, repo: Repo):
    user_data = await repo.get_courier(userid=m.chat.id)
    user_orders = await repo.get_couriers_orders(userid=m.chat.id)
    orders_number = len(user_orders)

    answer_message = f"""<b>Информация об аккаунте №{user_data['id']}</b>

🧑‍💼 <b>Общая информация</b>:
Тип аккаунта: <code>Курьер</code>
Статус: <code>{user_data['status']}</code>
Лицо: <code>{user_data['name']}</code>
Город: <code>{user_data['city'].title()}</code>
Номер: {user_data['number']}

📦 <b>Заказы</b>:
Общее кол-во выполненных заказов: {orders_number}"""

    await m.reply(text=answer_message,
                  reply_markup=personal_profile_kb)
