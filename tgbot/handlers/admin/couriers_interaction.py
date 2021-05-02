# change order courier
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils import exceptions
from aiogram.utils.exceptions import MessageNotModified

from tgbot.handlers.admin.manage_bot import manage_bot
from tgbot.keyboards.default.admin.check_courier import check_courier
from tgbot.keyboards.default.admin.return_to_menu import return_to_menu
from tgbot.keyboards.inline.admin.courier import courier_kb
from tgbot.keyboards.inline.customer.pagination import get_pages_keyboard
from tgbot.services import Repo
from tgbot.states.admin.new_courier import NewCourier


async def generate_courier_data_message(courier_data, orders):
    answer_message = f"""<b>🔎 Информация о курьере №{courier_data["id"]}</b>

🧑‍💼 ФИО: <code>{courier_data['name']}</code>
⏳ Статус: <code>{courier_data['status']}</code>
📱 Номер телефона: {courier_data['number']}

📦 Заказов взято: {len(orders)}
🆔 Профиль: <a href="tg://user?id={courier_data['id']}">Ссылка на профиль</a> """

    return answer_message


async def add_courier(c: CallbackQuery):
    await c.answer(text="Добавление нового курьера")
    await c.message.delete()
    await c.message.answer(text="🆔 Введите id курьера (/id):",
                           reply_markup=return_to_menu)
    await NewCourier.first()


async def courier_id(m: Message, repo: Repo, state: FSMContext):
    if m.text.isdigit():
        is_courier_exists = await repo.is_courier_exists(userid=m.text)
        if is_courier_exists:
            await m.answer(text="🚫 Данный курьер уже зарегистрирован.\n"
                                "Перейдите в меню управления курьерами для более подробной информации.")
            await state.finish()
            await manage_bot(m, repo)
            return
        await state.update_data(id=m.text)
        await m.answer(text="🧑‍💼 Введите <b>ФИО курьера</b>:",
                       reply_markup=return_to_menu)

        await NewCourier.next()
    else:
        await m.answer(text="🚫 <b>Введите корректный ID</b>")


async def courier_fio(m: Message, state: FSMContext):
    await state.update_data(name=m.text)
    await m.answer(text="📱 Введите <b>номер телефона курьера</b> (начиная с +7):")

    await NewCourier.next()


async def courier_number(m: Message, state: FSMContext):
    await state.update_data(number=m.text)
    await m.answer(text="💼 Отправьте <b>главную страницу паспорта курьера</b>:")
    await NewCourier.next()


async def courier_passport_main(m: Message, state: FSMContext):
    await state.update_data(passport_main=m.photo[0].file_id)
    await m.answer(text="💼 А теперь отправьте <b>страницу паспорта с пропиской курьера</b>:")
    await NewCourier.next()


async def courier_passport_registration(m: Message, state: FSMContext):
    await state.update_data(passport_registration=m.photo[0].file_id)
    await m.answer(text="💳 Отлично, отправьте <b>лицевую сторону водительского удостоверения курьера</b>:")
    await NewCourier.next()


async def courier_driving_license_front(m: Message, state: FSMContext):
    await state.update_data(driving_license_front=m.photo[0].file_id)
    await m.answer(text="💳 А теперь отправьте <b>обратную сторону водительского удостоверения курьера</b>:")
    await NewCourier.next()


async def courier_driving_license_back(m: Message, state: FSMContext):
    await state.update_data(driving_license_back=m.photo[0].file_id)
    courier_data = await state.get_data()

    media = types.MediaGroup()
    media.attach_photo(courier_data['passport_main'])
    media.attach_photo(courier_data['passport_registration'])
    media.attach_photo(courier_data['driving_license_front'])
    media.attach_photo(courier_data['driving_license_back'])

    await m.answer_media_group(media=media,
                               reply=True)
    await m.answer(text=f"""<b>Проверьте введённые данные:</b>

🧑‍💼 ФИО: <b>{courier_data['name']}</b>
📱 Номер телефона: <b>{courier_data['number']}</b>""",
                   reply_markup=check_courier)
    await NewCourier.next()


async def courier_choice(m: Message, repo: Repo, state: FSMContext):
    if m.text == "👌 Все правильно":
        courier_data = await state.get_data()
        partner_data = await repo.get_partner(userid=m.from_user.id)
        city = partner_data['city']
        courier = await repo.add_courier(userid=courier_data['id'], name=courier_data['name'], city=city,
                                         number=courier_data['number'], passport_main_id=courier_data['passport_main'],
                                         passport_registration_id=courier_data['passport_registration'],
                                         driver_license_front_id=courier_data['driving_license_front'],
                                         driver_license_back_id=courier_data['driving_license_back'], applied=True)
        await state.finish()
        try:
            await m.bot.send_message(chat_id=courier_data['id'], text=f"""
Здравствуйте, Вы назначены <b>курьером города {partner_data['city'].title()}!</b>
Используйте команду /start для обновления данных.""")
            await m.answer(
                text=f"""Вы добавили курьера!\nМы уже оповестили его о назначении.\n\n
{await generate_courier_data_message(courier[0], [])}""",
                reply_markup=ReplyKeyboardRemove())
        except exceptions.ChatNotFound:
            await m.answer(
                text=f"""<b>Вы добавили курьера, но мы не смогли уведомить его об этом!</b>\n
Отправьте курьеру <a href="https://t.me/dostavka30rus_bot">ссылку на бота</a> и попросите активировать его\n
{await generate_courier_data_message(courier[0], [])}""",
                reply_markup=ReplyKeyboardRemove())
        await manage_bot(m, repo)
    elif m.text == "🔄 Заполнить заново":
        await state.finish()
        await m.answer(text="🆔 Введите ID менеджера (/id):", reply_markup=return_to_menu)
        await NewCourier.first()

    elif m.text == "🏠 Вернуться в меню":
        await manage_bot(m, repo)


async def list_of_available_couriers(m: Message, repo: Repo):
    partner_data = await repo.get_partner(userid=m.chat.id)
    couriers_list = await repo.get_couriers_list(city=partner_data['city'])
    await m.answer(text="🚚 Курьеры:",
                   reply_markup=await get_pages_keyboard(key="couriers", array=couriers_list))


async def show_chosen_page_couriers(c: CallbackQuery, callback_data: dict, repo: Repo):
    partner_data = await repo.get_partner(c.message.chat.id)
    couriers_list = await repo.get_couriers_list(city=partner_data['city'])
    current_page = int(callback_data.get("page"))

    try:
        await c.message.edit_reply_markup(
            await get_pages_keyboard(key="couriers", array=couriers_list, page=current_page))
        await c.answer()
    except MessageNotModified:
        await c.answer(text="Страница не изменена")


async def show_courier(c: CallbackQuery, callback_data: dict, repo: Repo):
    await c.answer()
    courier_userid = callback_data['courier_id']

    answer_message = ""

    courier = await repo.get_courier(userid=courier_userid)
    courier_orders = await repo.get_couriers_orders(userid=courier['userid'])
    answer_message += await generate_courier_data_message(courier_data=courier, orders=courier_orders)
    await c.message.edit_text(text=answer_message, reply_markup=await courier_kb(courier_data=courier))


async def courier_action(c: CallbackQuery, callback_data: dict, repo: Repo):
    action = callback_data['action']
    if action == "activate":
        await repo.set_courier_apply_status(userid=callback_data['courier_id'], applied=True)
        await c.answer(text="Курьер активирован")
        courier_data = await repo.get_courier(userid=callback_data['courier_id'])
        courier_orders = await repo.get_couriers_orders(callback_data['courier_id'])
        await c.message.edit_text(text=await generate_courier_data_message(courier_data, orders=courier_orders),
                                  reply_markup=await courier_kb(courier_data))
    elif action == "deactivate":
        await repo.set_courier_apply_status(userid=callback_data['courier_id'], applied=False)
        await c.answer(text="Курьер деактивирован")
        courier_data = await repo.get_courier(userid=callback_data['courier_id'])
        courier_orders = await repo.get_couriers_orders(callback_data['courier_id'])
        await c.message.edit_text(text=await generate_courier_data_message(courier_data, orders=courier_orders),
                                  reply_markup=await courier_kb(courier_data))
    elif action == "delete":
        courier_data = await repo.get_courier(userid=callback_data['courier_id'])
        courier_orders = await repo.get_couriers_orders(callback_data['courier_id'])
        await repo.delete_courier(userid=callback_data['courier_id'])
        await c.answer(text="Курьер удален")
        try:
            await c.bot.send_message(chat_id=courier_data['userid'],
                                     text="<b>C ваc сняты права курьера.</b>\n\n"
                                          "<i>Если у вас есть вопросы, пожалуйста, обратитесь в тех. поддержку.</i>")
            await c.message.edit_text(f"""
<b>Партнер №{courier_data['id']} удален </b>

{await generate_courier_data_message(courier_data, courier_orders)}

Курьер получил уведомление о том, что он был удален.""")
        except exceptions.ChatNotFound:
            await c.message.edit_text(f"""
<b>Курьер №{courier_data['id']} удален </b>

{await generate_courier_data_message(courier_data, courier_orders)}

Курьер не получил уведомление о том, что он был удален (<i>бот не активирован</i>)""")
    elif action == "to_couriers":
        await c.answer()
        partner_data = await repo.get_partner(userid=c.message.chat.id)
        couriers_list = await repo.get_couriers_list(city=partner_data['city'])
        await c.message.edit_text(text="🚚 Курьеры:",
                                  reply_markup=await get_pages_keyboard(key="couriers", array=couriers_list))
