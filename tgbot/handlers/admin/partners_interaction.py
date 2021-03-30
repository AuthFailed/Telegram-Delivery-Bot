# change order courier
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

from tgbot.keyboards.inline.admin.partner import partner_kb
from tgbot.keyboards.inline.customer.pagination import get_pages_keyboard

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from tgbot.handlers.admin.manage_bot import manage_bot
from tgbot.keyboards.default.admin.check_partner import check_partner
from tgbot.keyboards.default.admin.return_to_menu import return_to_menu
from tgbot.services import Repo
from tgbot.states.admin.new_partner import NewPartner


async def generate_partner_data_message(partner_data, m: Message):
    orders_group = await m.bot.create_chat_invite_link(chat_id=partner_data['ordersgroupid']) if \
        partner_data['ordersgroupid'] is not None else "Не настроены"
    couriers_group = await m.bot.create_chat_invite_link(chat_id=partner_data['couriersgroupid']) if \
        partner_data['couriersgroupid'] is not None else "Не настроены"
    events_group = await m.bot.create_chat_invite_link(chat_id=partner_data['eventsgroupid']) if \
        partner_data['eventsgroupid'] is not None else "Не настроены"
    message_to_send = f"""<b>Партнер № {partner_data['id']}</b>

👨 <b>Общая информация</b>:
Город: <code>{partner_data['city']}</code>
Администратор: <a href="tg://user?id={partner_data['adminid']}">Ссылка на профиль</a> 

💬 <b>Чаты:</b>
Заказы: {orders_group}
Курьеры: {couriers_group}
События: {events_group}

Активирован: {"❌ Нет" if partner_data['isworking'] is False else "✅ Да"}"""
    return message_to_send


async def add_partner(c: CallbackQuery, repo: Repo):
    await c.answer(text="Добавление нового партнера")
    await c.message.delete()
    admin_info = await repo.get_partner(admin_id=c.message.chat.id)
    if admin_info['ismain']:
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
        is_partner_exists = await repo.is_partner_exists(partner_id=int(m.text))
        if is_partner_exists:
            await m.answer(text="🚫 Партнер с таким ID <b>уже существует</b> в базе данных.\n"
                                "Перейдите в меню управления партнерами для более подробной информации.")
            await state.finish()
            await manage_bot(m, repo)
            return
        await state.update_data(admin_id=m.text)
        partner_data = await state.get_data()
        await m.answer(text=f"""Проверьте введённые данные:
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
        await repo.add_partner(partner_id=partner_data['admin_id'],
                               city=partner_data['city'])
        await state.finish()
        await m.answer(text=f"""Вы успешно добавили нового партнера!
Подключенный город - <b>{partner_data['city'].title()}</b>.
Администратором назначен ID <b>{partner_data['admin_id']}</b>.
Отправьте партнеру <a href="https://t.me/dostavka30rus_bot">ссылку на бота</a> и попросите активировать его.""",
                       reply_markup=ReplyKeyboardRemove())

        partner_data = await repo.get_partner(city=partner_data['city'])
        print(partner_data)
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


async def show_chosen_page(c: CallbackQuery, callback_data: dict, repo: Repo):
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
    partner_id = callback_data['partner_id']

    answer_message = ""

    partner = await repo.get_partner(admin_id=partner_id)
    answer_message += await generate_partner_data_message(partner_data=partner, m=c.message)
    await c.message.edit_text(text=answer_message, reply_markup=await partner_kb(partner_data=partner))


async def partner_action(c: CallbackQuery, callback_data: dict, repo: Repo):
    action = callback_data['action']
    if action == "activate":
        await repo.change_partner_status(partner_id=callback_data['partner_id'], status=True)
        await c.answer(text="Партнер активирован")
        partner_data = await repo.get_partner(admin_id=callback_data['partner_id'])
        await c.message.edit_text(text=await generate_partner_data_message(partner_data, m=c.message),
                                  reply_markup=await partner_kb(partner_data))
    elif action == "deactivate":
        await repo.change_partner_status(partner_id=callback_data['partner_id'], status=False)
        await c.answer(text="Партнер деактивирован")
        partner_data = await repo.get_partner(admin_id=callback_data['partner_id'])
        await c.message.edit_text(text=await generate_partner_data_message(partner_data, m=c.message),
                                  reply_markup=await partner_kb(partner_data))
    elif action == "delete":
        partner_data = await repo.get_partner(admin_id=callback_data['partner_id'])
        await repo.delete_partner(admin_id=callback_data['partner_id'])
        await c.answer(text="Партнер удален")
        await c.message.edit_text(f"""
<b>Партнер №{partner_data['id']} удален </b>

👨 <b>Общая информация</b>:
Город: <code>{partner_data['city']}</code>
Администратор: <a href="tg://user?id={partner_data['adminid']}">Ссылка на профиль</a>""")

        await list_of_available_partners(m=c.message, repo=repo)
    elif action == "to_partners":
        await c.answer()
        partners_list = await repo.get_partners()
        if len(partners_list) > 0:
            await c.message.edit_text(text="🤝 Партнеры:",
                                      reply_markup=await get_pages_keyboard(key="partners", array=partners_list))
        else:
            await c.message.edit_text(text="Вы не добавили ни одного партнера.")
