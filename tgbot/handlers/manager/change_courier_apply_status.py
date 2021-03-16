from aiogram.types import CallbackQuery

from tgbot.services.repository import Repo


async def change_courier_apply_status(call: CallbackQuery, callback_data: dict, repo: Repo):
    await call.answer(
        text=f"Вы {'приняли' if callback_data.get('status') == 'True' else 'отклонили'} заявку №{callback_data.get('courier_id')}")
    courier_id = callback_data.get("courier_id")
    status = True if callback_data.get("status") == 'True' else False

    await repo.set_courier_apply_status(courier_id=courier_id, applied=status)
    courier_data = await repo.get_courier_by_userid(courier_id=courier_id)
    if status:
        await call.message.edit_text(text=f"""🚚 Курьер №{courier_data['id']} зарегистрирован

👨 Данные:
ФИО: <code>{courier_data['name']}</code>
Номер: {courier_data['number']}

⏳ Статус заявки:
✅ Одобрена""")
        await call.bot.send_message(chat_id=courier_data['userid'],
                                    text=f"""✅ <b>Ваша анкета одобрена</b>
Теперь вы будете получать заказы от менеджеров""")
    else:
        await call.message.edit_text(text=f"""🚚 Курьер №{courier_data['id']} зарегистрирован

👨 Данные:
ФИО: <code>{courier_data['name']}</code>
Номер: {courier_data['number']}

⏳ Статус заявки:
✖ Отклонена""")
        await call.bot.send_message(chat_id=courier_data['userid'],
                                    text=f"""✖ <b>Ваша анкета №{courier_data['id']} отклонена</b>
Если вы думаете, что вашу анкету отклонили по ошибке - свяжитесь с тех. поддержкой.""")
