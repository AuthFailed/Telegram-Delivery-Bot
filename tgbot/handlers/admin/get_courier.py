from aiogram.types import Message

from tgbot.services.repository import Repo


async def get_courier(m: Message, repo: Repo):
    args = m.get_args()
    if len(args) > 0:
        try:
             #requestor_data = await repo.get  # @TODO разобраться в виде реквестера
            courier_data = await repo.get_courier(serial_id=int(args))
            answer_message = f"""<b>🔎 Информация о курьере №{courier_data["id"]}</b>

Статус: {courier_data['status']}
ФИО: {courier_data['name']}
Номер телефона: {courier_data['number']}

📦 Заказов взято: {len(await repo.get_couriers_orders(userid=int(args)))}"""
            await m.reply(text=answer_message)
        except TypeError:
            await m.reply("<b>🔎 Курьера с таким номером не существует.</b>")
    else:
        answer_message = """Вводите команду в следующем формате:
<code>/курьер 41</code>
где 41 - номер курьера."""
        await m.reply(text=answer_message)
