from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.exceptions import BadRequest

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
        try:
            orders_group_link = await m.bot.create_chat_invite_link(chat_id=city_data['ordersgroupid'], member_limit=1)
            message_to_send += f'• <a href="{orders_group_link["invite_link"]}">Чат заказов</a>\n'
        except BadRequest:
            await m.bot.send_message(chat_id=city_data['userid'], text=f"Ваш новый менеджер №{manager_data['id']} не смог получить ссылку на чат с заказами.")
            await m.answer(text=f"Я хотел пригласить тебя в чат заказов, но у меня недостаточно прав. Я уже сообщил об этом администратору.")
    if city_data['couriersgroupid'] is not None:
        try:
            couriers_group_link = await m.bot.create_chat_invite_link(chat_id=city_data['couriersgroupid'], member_limit=1)
            message_to_send += f'• <a href="{couriers_group_link["invite_link"]}">Чат заявок курьеров</a>\n'
        except BadRequest:
            await m.bot.send_message(chat_id=city_data['userid'], text=f"Ваш новый менеджер №{manager_data['id']} не смог получить ссылку на чат с заявками курьеров.")
            await m.answer(text=f"Я хотел пригласить тебя в чат курьеров, но у меня недостаточно прав. Я уже сообщил об этом администратору.")
    if city_data['eventsgroupid'] is not None:
        try:
            events_group_link = await m.bot.create_chat_invite_link(chat_id=city_data['eventsgroupid'], member_limit=1)
            message_to_send += f'• <a href="{events_group_link["invite_link"]}">Чат событий</a>\n'
        except BadRequest:
            await m.bot.send_message(chat_id=city_data['userid'], text=f"Ваш новый менеджер №{manager_data['id']} не смог получить ссылку на чат с событями.")
            await m.answer(text=f"Я хотел пригласить тебя в чат событий, но у меня недостаточно прав. Я уже сообщил об этом администратору.")
    await m.answer(text=message_to_send)
