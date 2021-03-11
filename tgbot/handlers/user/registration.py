from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.default.courier.main_menu import main_menu as courier_main_menu
from tgbot.keyboards.default.user.main_menu import main_menu as user_main_menu
from tgbot.keyboards.default.user.return_to_menu import return_to_menu
from tgbot.keyboards.default.user.who_are_you import who_are_you
from tgbot.services.repository import Repo
from tgbot.states.user.registration import RegistrationUser, RegistrationCourier


async def reg_starts(m: Message):
    await m.answer(text="Зарегистрироваться как *компания*, *частное лицо* или *стать курьером*?",
                   reply_markup=who_are_you,
                   parse_mode="MarkdownV2")
    await RegistrationUser.first()


# user
async def reg_user_type(m: Message, repo: Repo, state: FSMContext):
    if m.text == "👥 Компания":
        await state.update_data(user_type="Компания")
        await m.reply(text="Введите *название вашей компании*:", reply_markup=return_to_menu,
                      parse_mode="MarkdownV2")
        await RegistrationUser.next()
    elif m.text == "👨‍💻 Частное лицо":
        await state.update_data(user_type='Частное лицо')
        await m.reply(text="👤 Введите *ФИО*:", reply_markup=return_to_menu,
                      parse_mode="MarkdownV2")
        await RegistrationUser.next()
    elif m.text == "🚚 Стать курьером":
        await state.finish()
        await m.reply(text="👤 Введите *ФИО*:", reply_markup=return_to_menu,
                      parse_mode="MarkdownV2")
        await RegistrationCourier.first()
    else:
        is_user_exists = await repo.is_user_exists(user_id=m.chat.id)
        await m.answer(text="Главное меню", reply_markup=await user_main_menu(reg=is_user_exists))
        await state.finish()


async def reg_user_name(m: Message, repo: Repo, state: FSMContext):
    if m.text == "Вернуться в меню":
        is_user_exists = await repo.is_user_exists(user_id=m.chat.id)
        await m.answer(text="Главное меню", reply_markup=await user_main_menu(reg=is_user_exists))
        await state.finish()
    else:
        async with state.proxy() as data:
            data['name'] = m.text
            user_type = data['user_type']

        if user_type == "Компания":
            await m.reply(text="📬 Введите *адрес компании*:",
                          reply_markup=return_to_menu,
                          parse_mode="MarkdownV2")
        else:
            await m.reply(text="📬 Введите *ваш адрес*:\n"
                               "Например: Пушкина 20",
                          reply_markup=return_to_menu,
                          parse_mode="MarkdownV2")
        await RegistrationUser.next()


async def reg_user_address(m: Message, repo: Repo, state: FSMContext):
    if m.text == "Вернуться в меню":
        is_user_exists = await repo.is_user_exists(user_id=m.chat.id)
        await m.answer(text="Главное меню", reply_markup=await user_main_menu(reg=is_user_exists))
        await state.finish()
    else:
        async with state.proxy() as data:
            data['address'] = m.text
            user_type = data['user_type']

        if user_type == "Компания":
            await m.reply(text="☎️ Введите *телефон компании*:",
                          reply_markup=return_to_menu,
                          parse_mode="MarkdownV2")
        else:
            await m.reply(text="☎️ Введите *ваш номер телефона*:",
                          reply_markup=return_to_menu,
                          parse_mode="MarkdownV2")
        await RegistrationUser.next()


async def reg_user_number(m: Message, repo: Repo, state: FSMContext):
    if m.text == "Вернуться в меню":
        is_user_exists = await repo.is_user_exists(user_id=m.chat.id)
        await m.answer(text="Главное меню", reply_markup=await user_main_menu(reg=is_user_exists))
        await state.finish()
    else:
        async with state.proxy() as data:
            data['number'] = m.text

        await repo.add_user(user_id=m.chat.id,
                            user_type=data['user_type'],
                            name=data['name'],
                            address=data['address'],
                            number=data['number'])
        await state.finish()
        await m.answer(text="👋 Вы зарегистрировались.\nТеперь вы можете оставить заявку!")
        await m.answer(text="Главное меню", reply_markup=await user_main_menu(reg=True))


# courier
async def reg_courier_name(m: Message, state: FSMContext):
    await state.update_data(name=m.text)

    await m.reply(text="☎️ Введите *номер телефона* \(начиная с \+7\):", reply_markup=return_to_menu,
                  parse_mode="MarkdownV2")
    await RegistrationCourier.next()


async def reg_courier_number(m: Message, state: FSMContext):
    await state.update_data(number=m.text)

    await m.reply(text="🗎 Отправьте *главную страницу паспорта*:",
                  reply_markup=return_to_menu,
                  parse_mode="MarkdownV2")
    await RegistrationCourier.next()


async def reg_courier_passport_main(m: Message, state: FSMContext):
    await state.update_data(passport_main=m.photo[0].file_id)

    await m.reply(text="🗎 А теперь отправьте *страницу паспорта с пропиской*:",
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

    await repo.add_courier(user_id=m.chat.id, name=courier_data['name'], number=courier_data['number'],
                           passport_main_id=courier_data['passport_main'],
                           passport_registration_id=courier_data['passport_registration'],
                           driver_license_back_id=courier_data['driving_license_front'],
                           driver_license_front_id=courier_data['driving_license_back'])
    await state.finish()
    await m.answer(text="👋 Вы зарегистрировались.\nС вами свяжется менеджер для проверки данных!")
    await m.answer(text="Главное меню", reply_markup=courier_main_menu)
