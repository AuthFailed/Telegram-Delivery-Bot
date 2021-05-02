# change order courier
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils import exceptions
from aiogram.utils.exceptions import MessageNotModified

from tgbot.handlers.admin.manage_bot import manage_bot
from tgbot.keyboards.default.admin.check_partner import check_partner
from tgbot.keyboards.default.admin.return_to_menu import return_to_menu
from tgbot.keyboards.inline.admin.partner import partner_kb
from tgbot.keyboards.inline.customer.pagination import get_pages_keyboard
from tgbot.services import Repo
from tgbot.states.admin.new_partner import NewPartner


async def generate_partner_data_message(partner_data, m: Message):
    if partner_data['ordersgroupid'] is not None:
        invite = await m.bot.create_chat_invite_link(chat_id=partner_data['ordersgroupid'])
        chat_link = invite['invite_link']
        orders_group = f'<a href="{chat_link}">Ссылка</a>'
    else:
        orders_group = "Не настроен"

    if partner_data['couriersgroupid'] is not None:
        invite = await m.bot.create_chat_invite_link(chat_id=partner_data['couriersgroupid'])
        chat_link = invite['invite_link']
        couriers_group = f'<a href="{chat_link}">Ссылка</a>'
    else:
        couriers_group = "Не настроен"

    if partner_data['eventsgroupid'] is not None:
        invite = await m.bot.create_chat_invite_link(chat_id=partner_data['eventsgroupid'])
        chat_link = invite['invite_link']
        events_group = f'<a href="{chat_link}">Ссылка</a>'
    else:
        events_group = "Не настроен"

    message_to_send = f"""<b>Партнер №{partner_data['id']}</b>

🧑‍💼 <b>Общая информация</b>:
Город: <code>{partner_data['city'].title()}</code>

💬 <b>Чаты:</b>
🛍 Заказы: {orders_group}
🚚 Курьеры: {couriers_group}
🎃 События: {events_group}

Активирован: {"❌ Нет" if partner_data['working'] is False else "✅ Да"}
🆔 Администратор: <a href="tg://user?id={partner_data['adminid']}">Ссылка на профиль</a> """
    return message_to_send


async def add_partner(c: CallbackQuery, repo: Repo):
    await c.answer(text="Добавление нового партнера")
    await c.message.delete()
    admin_info = await repo.get_partner(userid=c.message.chat.id)
    if admin_info['main']:
        await c.message.answer(text="🏙️ Введите название города-партнера:",
                               reply_markup=return_to_menu)
        await NewPartner.first()
    else:
        await c.message.answer(text="У Вас нет доступа к функционалу <b>главного администратора</b>!")


async def partner_city(m: Message, repo: Repo, state: FSMContext):
    is_city_exists = await repo.is_partner_exists(city=m.text.lower())
    if is_city_exists:
        await m.answer(text="🚫 Партнер с таким городом <b>уже существует</b> в базе данных.\n"
                            "Перейдите в меню управления партнерами для более подробной информации.")
        await state.finish()
        await manage_bot(m, repo)
        return
    await state.update_data(city=m.text.lower())
    await m.answer(text="👑 Введите ID администратора:",
                   reply_markup=return_to_menu)

    await NewPartner.next()


async def partner_id(m: Message, repo: Repo, state: FSMContext):
    if m.text.isdigit():
        is_partner_exists = await repo.is_partner_exists(userid=int(m.text))
        if is_partner_exists:
            await m.answer(text="🚫 Партнер с таким ID <b>уже существует</b> в базе данных.\n"
                                "Перейдите в меню управления партнерами для более подробной информации.")
            await state.finish()
            await manage_bot(m, repo)
            return
        await state.update_data(admin_id=m.text)
        partner_data = await state.get_data()
        await m.answer(text=f"""<b>Проверьте введённые данные:</b>
        
👑 ID администратора: <b>{partner_data['admin_id']}</b>
🏙 Город: <b>{partner_data['city'].title()}</b>
    """,
                       reply_markup=check_partner)
        await NewPartner.next()
    else:
        await m.answer(text="🚫 <b>Введите корректный ID</b>")


async def partner_choice(m: Message, repo: Repo, state: FSMContext):
    if m.text == "👌 Все правильно":
        partner_data = await state.get_data()
        await repo.add_partner(userid=partner_data['admin_id'], city=partner_data['city'].lower())
        await state.finish()
        try:
            await m.bot.send_message(chat_id=partner_data['admin_id'], text=f"""
Здравствуйте, Вы назначены <b>администратором города {partner_data['city'].title()}!</b>
Используйте команду /start для обновления данных.""")
            await m.answer(text=f"""Вы добавили партнера!
Подключенный город - <b>{partner_data['city'].title()}</b>.
Администратором назначен ID <b>{partner_data['admin_id']}</b>.""",
                           reply_markup=ReplyKeyboardRemove())
        except exceptions.ChatNotFound:
            text = f"""<b>Вы добавили партнера, но мы не смогли уведомить его об этом!</b>\n
Отправьте партнеру <a href="https://t.me/dostavka30rus_bot">ссылку на бота</a> и попросите активировать его"""
            await m.answer(text=text,
                           reply_markup=ReplyKeyboardRemove())
            await manage_bot(m, repo)
        partner_data = await repo.get_partner(city=partner_data['city'])
        await m.answer(text=await generate_partner_data_message(partner_data=partner_data, m=m))

        await manage_bot(m, repo)

    elif m.text == "🔄 Заполнить заново":
        await state.finish()
        await m.answer(text="🏙️ Введите название города-партнера:", reply_markup=return_to_menu)
        await NewPartner.first()

    elif m.text == "🏠 Вернуться в меню":
        await manage_bot(m, repo)


async def list_of_available_partners(m: Message, repo: Repo):
    partners_list = await repo.get_partners()
    await m.answer(text="🤝 Партнеры:",
                   reply_markup=await get_pages_keyboard(key="partners", array=partners_list))


async def show_chosen_page_partners(c: CallbackQuery, callback_data: dict, repo: Repo):
    partners_list = await repo.get_partners()
    current_page = int(callback_data.get("page"))

    try:
        await c.message.edit_reply_markup(
            await get_pages_keyboard(key="partners", array=partners_list, page=current_page))
        await c.answer()
    except MessageNotModified:
        await c.answer(text="Страница не изменена")


async def show_partner(c: CallbackQuery, callback_data: dict, repo: Repo):
    await c.answer()
    partner_userid = callback_data['partner_id']

    answer_message = ""

    partner = await repo.get_partner(userid=partner_userid)
    answer_message += await generate_partner_data_message(partner_data=partner, m=c.message)
    await c.message.edit_text(text=answer_message, reply_markup=await partner_kb(partner_data=partner))


async def partner_action(c: CallbackQuery, callback_data: dict, repo: Repo):
    action = callback_data['action']
    if action == "activate":
        await repo.change_partner_status(partner_userid=callback_data['partner_id'], status=True)
        await c.answer(text="Партнер активирован")
        partner_data = await repo.get_partner(userid=callback_data['partner_id'])
        await c.message.edit_text(text=await generate_partner_data_message(partner_data, m=c.message),
                                  reply_markup=await partner_kb(partner_data))
    elif action == "deactivate":
        await repo.change_partner_status(partner_userid=callback_data['partner_id'], status=False)
        await c.answer(text="Партнер деактивирован")
        partner_data = await repo.get_partner(userid=callback_data['partner_id'])
        await c.message.edit_text(text=await generate_partner_data_message(partner_data, m=c.message),
                                  reply_markup=await partner_kb(partner_data))
    elif action == "delete":
        partner_data = await repo.get_partner(userid=callback_data['partner_id'])
        await repo.delete_partner(userid=callback_data['partner_id'])
        await c.answer(text="Партнер удален")
        try:
            await c.bot.send_message(chat_id=partner_data['adminid'],
                                     text="<b>Ваш город удален, с вам сняты права администратора.</b>\n\n"
                                          "<i>Если у вас есть вопросы, пожалуйста, обратитесь в тех. поддержку.</i>")
            await c.message.edit_text(f"""
<b>Партнер №{partner_data['id']} удален </b>

🧑‍💼 <b>Общая информация</b>:
Город: <code>{partner_data['city'].title()}</code>
Администратор: <a href="tg://user?id={partner_data['adminid']}">Ссылка на профиль</a>

Партнер получил уведомление о том, что он был удален.""")
        except exceptions.ChatNotFound:
            await c.message.edit_text(f"""
<b>Партнер №{partner_data['id']} удален </b>

🧑‍💼 <b>Общая информация</b>:
Город: <code>{partner_data['city'].title()}</code>
Администратор: <a href="tg://user?id={partner_data['adminid']}">Ссылка на профиль</a>

Партнер не получил уведомление о том, что он был удален (<i>бот не активирован<i>)""")

        await list_of_available_partners(m=c.message, repo=repo)
    elif action == "to_partners":
        await c.answer()
        partners_list = await repo.get_partners()
        await c.message.edit_text(text="🤝 Партнеры:",
                                  reply_markup=await get_pages_keyboard(key="partners", array=partners_list))


async def activate_partner(m: Message, repo: Repo):
    partner_data = await repo.get_partner(userid=m.chat.id)
    if partner_data['working'] is True:
        await m.answer(text="Ничего не изменилось, бот уже активирован.")
        return
    if partner_data['ordersgroupid'] is None or partner_data['couriersgroupid'] is None \
            or partner_data['eventsgroupid'] is None:
        await m.answer("Вы не можете активировать бота пока не настроите необходимые группы.\n"
                       "Используйте команду /setting_groups для более подробной информации.")
        return
    await repo.change_partner_status(partner_userid=m.chat.id, status=True)
    await m.answer(text="<b>Бот активирован!</b>\n\n"
                        "Ваш город появится на этапе регистрации, а старые пользователи смогут создать заказ.")
    await manage_bot(m, repo)


async def deactivate_partner(m: Message, repo: Repo):
    partner_data = await repo.get_partner(userid=m.chat.id)
    if partner_data['working'] is False:
        await m.answer(text="Ничего не изменилось, бот уже деактивирован.")
        return
    await repo.change_partner_status(partner_userid=m.chat.id, status=False)
    await m.answer(text="<b>Бот деактивирован!</b>\n\n"
                        "Ваш город не будет показан на этапе регистрации, а старые пользователи не смогут создать "
                        "заказ.")
    await manage_bot(m, repo)
