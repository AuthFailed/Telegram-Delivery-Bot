from aiogram.types import Message

from tgbot.services.repository import Repo


async def get_courier(m: Message, repo: Repo):
    args = m.get_args()
    if len(args) > 0:
        try:
            courier_data = await repo.get_courier_by_id(courier_id=int(args))
            answer_message = f"""*🔎 Информация о заказчике №{courier_data["id"]}*

ФИО: {courier_data['name']}
Номер телефона: {courier_data['number']}

📦 Заказов взято: {len(await repo.get_couriers_orders(courier_id=int(args)))}"""
            await m.reply(text=answer_message, parse_mode='Markdown')
        except TypeError:
            await m.reply("*🔎 Курьера с таким номером не существует.*",
                          parse_mode='Markdown')
    else:
        answer_message = """Вводите команду /курьер в следующем формате:
`/курьер 41`
где 41 - номер курьера."""
        await m.reply(text=answer_message, parse_mode='Markdown')
