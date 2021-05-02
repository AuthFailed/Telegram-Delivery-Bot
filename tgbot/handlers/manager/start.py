from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from tgbot.services.repository import Repo


async def start(m: Message, repo: Repo, state: FSMContext = None):
    if state is not None:
        await state.finish()

    await m.answer(text=f"Привет, <b>менеджер</b>!\n"
                        f"У тебя пока нет личного меню, но есть пара команд: /заказчик, /заказ и /курьер",
                   reply_markup=ReplyKeyboardRemove())
    manager_data = await repo.get_manager(userid=m.chat.id)
    city_data = await repo.get_partner(city=manager_data['city'])

    message_to_send = "Всю нужную для работы информацию ты найдешь в следующих чатах:\n"
    if city_data['ordersgroupid'] is not None:
        orders_group_link = await m.bot.create_chat_invite_link(chat_id=city_data['ordersgroupid'], member_limit=1)
        message_to_send += f'• <a href="{orders_group_link["invite_link"]}">Чат заказов</a>\n'
    if city_data['couriersgroupid'] is not None:
        couriers_group_link = await m.bot.create_chat_invite_link(chat_id=city_data['couriersgroupid'], member_limit=1)
        message_to_send += f'• <a href="{couriers_group_link["invite_link"]}">Чат заявок курьеров</a>\n'
    if city_data['eventsgroupid'] is not None:
        events_group_link = await m.bot.create_chat_invite_link(chat_id=city_data['eventsgroupid'], member_limit=1)
        message_to_send += f'• <a href="{events_group_link["invite_link"]}">Чат событий</a>\n'
    await m.answer(text=message_to_send)
