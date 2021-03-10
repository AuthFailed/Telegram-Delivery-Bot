from aiogram.types import Message

from tgbot.keyboards.default.user.personal_profile import personal_profile_kb
from tgbot.services.repository import Repo


async def personal_profile(m: Message, repo: Repo):
    user_data = await repo.get_user(user_id=m.chat.id)
    user_orders = await repo.get_user_orders(user_id=m.chat.id)
    orders_number = len(user_orders)

    answer_message = f"""*Информация об аккаунте №{user_data['id']}*

👨 *Общая информация*:
Тип аккаунта: `{user_data['usertype']}`
Имя: `{user_data['name']}`
Адрес: `{user_data['address']}`
Номер: `{user_data['number']}`

📦 *Заказы*:
Общее кол\-во заказов: {orders_number}"""

    await m.reply(text=answer_message,
                  reply_markup=personal_profile_kb,
                  parse_mode='MARKDOWNV2')
