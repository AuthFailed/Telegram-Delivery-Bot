from aiogram.types import Message

from tgbot.services.repository import Repo


async def get_customer(m: Message, repo: Repo):
    args = m.get_args()
    if len(args) > 0:
        try:
            courier_data = await repo.get_customer(id=int(args))
            answer_message = f"""<b>🔎 Информация о заказчике №{courier_data["id"]}</b>

ФИО: {courier_data['name']}
Номер телефона: {courier_data['number']}

📦 Заказов взято: {len(await repo.get_couriers_orders(courier_id=int(args)))}"""
            await m.reply(text=answer_message)
        except TypeError:
            await m.reply("<b>🔎 Заказчика с таким номером не существует.</b>")
    else:
        answer_message = """Вводите команду в следующем формате:
<code>/заказчик 41</code>
где 41 - номер заказчика."""
        await m.reply(text=answer_message)
