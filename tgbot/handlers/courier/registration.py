from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.config import load_config
from tgbot.keyboards.default.courier.main_menu import main_menu
from tgbot.keyboards.default.user.return_to_menu import return_to_menu
from tgbot.keyboards.inline.manager.accept_courier import courier_request_kb
from tgbot.services.event_handlers import new_courier
from tgbot.services.repository import Repo
from tgbot.states.user.registration import RegistrationCourier


async def reg_courier_name(m: Message, state: FSMContext):
    await state.update_data(name=m.text)

    await m.reply(text="☎️ Введите *номер телефона* \(начиная с \+7\):", reply_markup=return_to_menu,
                  parse_mode="MarkdownV2")
    await RegistrationCourier.next()


async def reg_courier_number(m: Message, state: FSMContext):
    await state.update_data(number=m.text)

    await m.reply(text="💼 Отправьте *главную страницу паспорта*:",
                  reply_markup=return_to_menu,
                  parse_mode="MarkdownV2")
    await RegistrationCourier.next()


async def reg_courier_passport_main(m: Message, state: FSMContext):
    await state.update_data(passport_main=m.photo[0].file_id)

    await m.reply(text="💼 А теперь отправьте *страницу паспорта с пропиской*:",
                  reply_markup=return_to_menu,
                  parse_mode="MarkdownV2")
    await RegistrationCourier.next()


async def reg_courier_passport_registration(m: Message, state: FSMContext):
    await state.update_data(passport_registration=m.photo[0].file_id)

    await m.reply(text="💳 Отлично, отправьте *лицевую сторону водительского удостоверения*:",
                  reply_markup=return_to_menu,
                  parse_mode="MarkdownV2")
    await RegistrationCourier.next()


async def reg_courier_driving_license_front(m: Message, state: FSMContext):
    await state.update_data(driving_license_front=m.photo[0].file_id)

    await m.reply("💳 А теперь отправьте *обратную сторону водительского удостоверения*:", reply_markup=return_to_menu,
                  parse_mode="MarkdownV2")
    await RegistrationCourier.next()


async def reg_courier_driving_license_back(m: Message, repo: Repo, state: FSMContext):
    async with state.proxy() as data:
        data['driving_license_back'] = m.photo[0].file_id
        courier_data = data

    courier_db_data = await repo.add_courier(user_id=m.chat.id, name=courier_data['name'],
                                             number=courier_data['number'],
                                             passport_main_id=courier_data['passport_main'],
                                             passport_registration_id=courier_data['passport_registration'],
                                             driver_license_back_id=courier_data['driving_license_front'],
                                             driver_license_front_id=courier_data['driving_license_back'])
    await state.finish()
    await m.answer(text="👋 Вы зарегистрировались.\nС вами свяжется менеджер для проверки данных!")
    await m.answer(text="Главное меню", reply_markup=main_menu)

    config = load_config("bot.ini")
    media = types.MediaGroup()
    media.attach_photo(courier_db_data[0]['passportmain'])
    media.attach_photo(courier_db_data[0]['passportregistration'])
    media.attach_photo(courier_db_data[0]['driverlicensefront'])
    media.attach_photo(courier_db_data[0]['driverlicenseback'])

    courier_message = f"""*🚚 Курьер №{courier_db_data[0]['id']} зарегистрирован*

👨 Данные:
ФИО: `{courier_data['name']}`
Номер: {courier_data['number']}

⏳ Статус заявки:
_На рассмотрении_"""
    courier_data_message = await m.bot.send_message(chat_id=config.tg_bot.couriers_group,
                                                    text=courier_message,
                                                    reply_markup=await courier_request_kb(courier_id=m.chat.id),
                                                    parse_mode="Markdown")
    await new_courier(m=m, courier_data=courier_db_data[0])
    await courier_data_message.answer_media_group(media=media,
                                                  reply=True)
