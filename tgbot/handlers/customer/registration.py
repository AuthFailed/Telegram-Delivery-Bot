from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.default.user.main_menu import main_menu as user_main_menu
from tgbot.keyboards.default.user.return_to_menu import return_to_menu
from tgbot.keyboards.default.user.who_are_you import who_are_you
from tgbot.services.event_handlers import new_customer
from tgbot.services.repository import Repo
from tgbot.states.user.registration import RegistrationUser, RegistrationCourier


async def reg_starts(m: Message):
    await m.answer(text="Зарегистрироваться как *компания*, *частное лицо* или *стать курьером*?",
                   reply_markup=who_are_you,
                   parse_mode="MarkdownV2")
    await RegistrationUser.first()


# user
async def reg_type(m: Message, repo: Repo, state: FSMContext):
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


async def reg_name(m: Message, repo: Repo, state: FSMContext):
    if m.text == "Вернуться в меню":
        is_user_exists = await repo.is_user_exists(user_id=m.chat.id)
        await m.answer(text="Главное меню", reply_markup=await user_main_menu(reg=is_user_exists))
        await state.finish()
    else:
        async with state.proxy() as data:
            data['name'] = m.text
            user_type = data['type']

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


async def reg_address(m: Message, repo: Repo, state: FSMContext):
    if m.text == "Вернуться в меню":
        is_user_exists = await repo.is_user_exists(user_id=m.chat.id)
        await m.answer(text="Главное меню", reply_markup=await user_main_menu(reg=is_user_exists))
        await state.finish()
    else:
        async with state.proxy() as data:
            data['address'] = m.text
            user_type = data['type']

        if user_type == "Компания":
            await m.reply(text="☎️ Введите *телефон компании*:",
                          reply_markup=return_to_menu,
                          parse_mode="MarkdownV2")
        else:
            await m.reply(text="☎️ Введите *ваш номер телефона*:",
                          reply_markup=return_to_menu,
                          parse_mode="MarkdownV2")
        await RegistrationUser.next()


async def reg_number(m: Message, repo: Repo, state: FSMContext):
    if m.text == "Вернуться в меню":
        is_user_exists = await repo.is_user_exists(user_id=m.chat.id)
        await m.answer(text="Главное меню", reply_markup=await user_main_menu(reg=is_user_exists))
        await state.finish()
    else:
        async with state.proxy() as data:
            data['number'] = m.text

        customer_id = await repo.add_user(user_id=m.chat.id,
                                          user_type=data['type'],
                                          name=data['name'],
                                          address=data['address'],
                                          number=data['number'])
        await state.finish()
        await new_customer(m=m, customer_data=data, customer_id=customer_id)
        await m.answer(text="👋 Вы зарегистрировались.\nТеперь вы можете оставить заказ!")
        await m.answer(text="Главное меню", reply_markup=await user_main_menu(reg=True))
