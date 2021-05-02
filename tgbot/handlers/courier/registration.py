from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils import exceptions

from tgbot.handlers.courier.start import start
from tgbot.keyboards.default.courier.main_menu import main_menu
from tgbot.keyboards.default.customer.return_to_menu import return_to_menu
from tgbot.keyboards.default.customer.send_number import ask_phone_number
from tgbot.keyboards.inline.customer.pagination import get_pages_keyboard
from tgbot.keyboards.inline.manager.accept_courier import courier_request_kb
from tgbot.services.event_handlers import new_courier
from tgbot.services.repository import Repo
from tgbot.states.customer.registration import RegistrationCourier


async def reg_name(m: Message, repo: Repo, state: FSMContext):
    await state.update_data(name=m.text)
    cities_list = await repo.get_available_cities()
    if len(cities_list) > 0:
        await m.reply(text="📬 Выберите ваш город из списка",
                      reply_markup=await get_pages_keyboard(array=cities_list, width=2, items_per_page=10,
                                                            key="cities"))
        await RegistrationCourier.next()
    else:
        await m.answer(text="В данный момент ни один город не активен. Регистрация будет сброшена.")
        await start(m, state)


async def show_chosen_page_city(c: CallbackQuery, callback_data: dict, repo: Repo, state: FSMContext):
    cities_list = await repo.get_available_cities()
    current_page = int(callback_data.get("page"))

    try:
        await c.message.edit_reply_markup(
            await get_pages_keyboard(cities_list, width=2, items_per_page=10, page=current_page, key="cities"))
        await c.answer()
    except exceptions.MessageNotModified:
        await c.answer(text="Страница не изменена")


async def set_city(c: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = callback_data['city_name'].lower()
    # await state.update_data(city=callback_data['city_name'].lower())
    await c.answer(text=f"Выбран город {callback_data['city_name']}")

    await c.message.reply(text="📱️ Введите <b>номер телефона</b> (начиная с +7):", reply_markup=ask_phone_number)
    await RegistrationCourier.next()


async def reg_number(m: Message, state: FSMContext):
    await state.update_data(number=m.text)

    await m.reply(text="💼 Отправьте <b>главную страницу паспорта</b>:",
                  reply_markup=return_to_menu)
    await RegistrationCourier.next()


async def reg_passport_main(m: Message, state: FSMContext):
    await state.update_data(passport_main=m.photo[0].file_id)

    await m.reply(text="💼 А теперь отправьте <b>страницу паспорта с пропиской</b>:",
                  reply_markup=return_to_menu)
    await RegistrationCourier.next()


async def reg_passport_registration(m: Message, state: FSMContext):
    await state.update_data(passport_registration=m.photo[0].file_id)

    await m.reply(text="💳 Отлично, отправьте <b>лицевую сторону водительского удостоверения</b>:",
                  reply_markup=return_to_menu)
    await RegistrationCourier.next()


async def reg_driving_license_front(m: Message, state: FSMContext):
    await state.update_data(driving_license_front=m.photo[0].file_id)

    await m.reply("💳 А теперь отправьте <b>обратную сторону водительского удостоверения</b>:",
                  reply_markup=return_to_menu)
    await RegistrationCourier.next()


async def reg_driving_license_back(m: Message, repo: Repo, state: FSMContext):
    async with state.proxy() as data:
        data['driving_license_back'] = m.photo[0].file_id
        courier_data = data

    courier_db_data = await repo.add_courier(userid=m.chat.id,
                                             name=courier_data['name'],
                                             city=courier_data['city'],
                                             number=courier_data['number'],
                                             passport_main_id=courier_data['passport_main'],
                                             passport_registration_id=courier_data['passport_registration'],
                                             driver_license_front_id=courier_data['driving_license_back'],
                                             driver_license_back_id=courier_data['driving_license_front'])
    await state.finish()
    await m.answer(text="👋 Вы зарегистрировались.\nС вами свяжется менеджер для проверки данных!")
    await m.answer(text="Главное меню", reply_markup=main_menu)

    media = types.MediaGroup()
    media.attach_photo(courier_db_data[0]['passportmain'])
    media.attach_photo(courier_db_data[0]['passportregistration'])
    media.attach_photo(courier_db_data[0]['driverlicensefront'])
    media.attach_photo(courier_db_data[0]['driverlicenseback'])

    courier_message = f"""<b>🚚 Курьер №{courier_db_data[0]['id']} зарегистрирован</b>

👨 Данные:
ФИО: <code>{courier_data['name']}</code>
Город: <code>{courier_data['city'].title()}</code>
Номер: {courier_data['number']}

⏳ Статус заявки:
<i>На рассмотрении</i>"""

    city_data = await repo.get_partner(city=courier_data['city'])
    courier_data_message = await m.bot.send_message(chat_id=city_data['couriersgroupid'],
                                                    text=courier_message,
                                                    reply_markup=await courier_request_kb(courier_id=m.chat.id))
    if city_data['couriersgroupid'] is not None:
        await new_courier(m=m, courier_data=courier_db_data[0])
    await courier_data_message.answer_media_group(media=media,
                                                  reply=True)
