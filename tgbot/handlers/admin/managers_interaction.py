# change order courier
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils import exceptions
from aiogram.utils.exceptions import MessageNotModified

from tgbot.handlers.admin.manage_bot import manage_bot
from tgbot.handlers.admin.start import start
from tgbot.keyboards.default.admin.check_manager import check_manager
from tgbot.keyboards.default.admin.return_to_menu import return_to_menu
from tgbot.keyboards.inline.admin.manager import manager_kb
from tgbot.keyboards.inline.customer.pagination import get_pages_keyboard
from tgbot.services import Repo
from tgbot.states.admin.new_manager import NewManager


async def generate_manager_data_message(manager_data):
    message_to_send = f"""<b>Менеджер №{manager_data['id']}</b>

🧑‍💼 <b>Общая информация</b>:
Фио: <code>{manager_data['name']}</code>
Город: <code>{manager_data['city'].title()}</code>
Номер: {manager_data['number']}

Профиль: <a href="tg://user?id={manager_data['userid']}">Ссылка на профиль</a> """

    return message_to_send


async def add_manager(c: CallbackQuery):
    await c.answer(text="Добавление нового менеджера")
    await c.message.delete()
    await c.message.answer(text="🆔 Введите ID менеджера (/id):",
                           reply_markup=return_to_menu)
    await NewManager.first()


async def manager_id(m: Message, repo: Repo, state: FSMContext):
    if m.text.isdigit():
        is_manager_exists = await repo.is_courier_exists(userid=m.text)
        if is_manager_exists:
            await m.answer(text="🚫 Данный менеджер уже зарегистрирован.\n"
                                "Перейдите в меню управления менеджерами для более подробной информации.")
            await state.finish()
            await manage_bot(m, repo)
            return
        await state.update_data(manager_id=m.text)
        await m.answer(text="👨‍💼 Введите ФИО менеджера:",
                       reply_markup=return_to_menu)

        await NewManager.next()
    else:
        await m.answer(text="🚫 <b>Введите корректный ID</b>")


async def manager_fio(m: Message, state: FSMContext):
    await state.update_data(fio=m.text)
    await m.answer(text="📱️ Введите <b>номер телефона</b> менеджера (начиная с +7):")

    await NewManager.next()


async def manager_number(m: Message, state: FSMContext):
    await state.update_data(number=m.text)
    manager_data = await state.get_data()

    await m.answer(text=f"""Проверьте введённые данные:

👨‍💼 Фио: <b>{manager_data['fio']}</b>
📱 Номер: <b>{manager_data['number']}</b>
🆔 Профиль менеджера: <a href="tg://user?id={manager_data['manager_id']}">Ссылка на профиль</a> 
""",
                   reply_markup=check_manager)
    await NewManager.next()


async def manager_choice(m: Message, repo: Repo, state: FSMContext):
    if m.text == "👌 Все правильно":
        partner_data = await repo.get_partner(userid=m.from_user.id)
        city = partner_data['city']
        manager_data = await state.get_data()
        await repo.add_manager(userid=manager_data['manager_id'], name=manager_data['fio'], city=city,
                               number=manager_data['number'])
        await state.finish()
        try:
            await m.bot.send_message(chat_id=manager_data['manager_id'], text=f"""
Здравствуйте, Вы назначены <b>менеджером города {partner_data['city'].title()}!</b>
Используйте команду /start для обновления данных.""")
            await m.answer(text=f"""Вы добавили менеджера!

{await generate_manager_data_message(manager_data)}

Менеджер уже получил уведомление о своем назначении.""",
                           reply_markup=ReplyKeyboardRemove())
        except exceptions.ChatNotFound:
            await m.answer(text=f"""<b>Вы добавили менеджера, но мы не смогли уведомить его об этом!</b>\n
Отправьте менеджеру <a href="https://t.me/dostavka30rus_bot">ссылку на бота</a> и попросите активировать его""",
                           reply_markup=ReplyKeyboardRemove())
            await manage_bot(m, repo)
    elif m.text == "🔄 Заполнить заново":
        await state.finish()
        await m.answer(text="🆔 Введите ID менеджера (/id):", reply_markup=return_to_menu)
        await NewManager.first()

    elif m.text == "🏠 Вернуться в меню":
        await start(m, repo, state)


async def list_of_available_managers(m: Message, repo: Repo):
    partner_data = await repo.get_partner(userid=m.chat.id)
    managers_list = await repo.get_managers_list(city=partner_data['city'])
    await m.answer(text="👨‍💼 Менеджеры:",
                   reply_markup=await get_pages_keyboard(key="managers", array=managers_list))


async def show_chosen_page_managers(c: CallbackQuery, callback_data: dict, repo: Repo):
    partner_data = await repo.get_partner(userid=c.message.chat.id)
    managers_list = await repo.get_managers_list(city=partner_data['city'])
    current_page = int(callback_data.get("page"))

    try:
        await c.message.edit_reply_markup(
            await get_pages_keyboard(key="managers", array=managers_list, page=current_page))
        await c.answer()
    except MessageNotModified:
        await c.answer(text="Страница не изменена")


async def show_manager(c: CallbackQuery, callback_data: dict, repo: Repo):
    await c.answer()
    manager_userid = callback_data['manager_id']

    manager = await repo.get_manager(userid=manager_userid)
    answer_message = await generate_manager_data_message(manager_data=manager)
    await c.message.edit_text(text=answer_message, reply_markup=await manager_kb(manager_data=manager))


async def manager_action(c: CallbackQuery, callback_data: dict, repo: Repo):
    action = callback_data['action']
    if action == "delete":
        manager_data = await repo.get_manager(userid=callback_data['manager_id'])
        await repo.delete_manager(userid=callback_data['manager_id'])
        await c.answer(text="Менеджер удален")
        try:
            await c.bot.send_message(chat_id=manager_data['userid'],
                                     text="<b>С вас сняты права менеджера.</b>\n\n"
                                          "<i>Если у вас есть вопросы, пожалуйста, обратитесь в отделение своего города.</i>")
            await c.message.edit_text(f"""
<b>Менеджер №{manager_data['id']} удален </b>

👨‍💼 Фио: <b>{manager_data['name']}</b>
📱 Номер: <b>{manager_data['number']}</b>
🆔 Профиль менеджера: <a href="tg://user?id={manager_data['userid']}">Ссылка на профиль</a>

""")
        except exceptions.ChatNotFound:
            await c.message.edit_text(f"""
<b>Менеджер №{manager_data['id']} удален </b>

👨‍💼 Фио: <b>{manager_data['name']}</b>
📱Номер: <b>{manager_data['number']}</b>
🆔 Профиль менеджера: <a href="tg://user?id={manager_data['userid']}">Ссылка на профиль</a>

            """)

        await list_of_available_managers(m=c.message, repo=repo)
    elif action == "to_managers":
        await c.answer()
        partner_data = await repo.get_partner(userid=c.message.chat.id)
        managers_list = await repo.get_managers_list(city=partner_data['city'])
        await c.message.edit_text(text="👨‍💼 Менеджеры:",
                                  reply_markup=await get_pages_keyboard(key="managers", array=managers_list))
