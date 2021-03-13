from aiogram.types import Message

from tgbot.keyboards.default.courier.personal_profile import personal_profile_kb
from tgbot.services.repository import Repo


async def personal_profile(m: Message, repo: Repo):
    user_data = await repo.get_courier(courier_id=m.chat.id)
    user_orders = await repo.get_couriers_orders(courier_id=m.chat.id)
    orders_number = len(user_orders)

    answer_message = f"""*Информация об аккаунте №{user_data['id']}*

👨 *Общая информация*:
Тип аккаунта: `Курьер`
Имя: `{user_data['name']}`
Номер: `{user_data['number']}`

📦 *Заказы*:
Общее кол\-во выполненных заказов: {orders_number}"""

    await m.reply(text=answer_message,
                  reply_markup=personal_profile_kb,
                  parse_mode='MARKDOWNV2')
