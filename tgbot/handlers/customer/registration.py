from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

from tgbot.handlers.customer.start import start
from tgbot.keyboards.default.customer.main_menu import main_menu as user_main_menu
from tgbot.keyboards.default.customer.return_to_menu import return_to_menu
from tgbot.keyboards.default.customer.send_number import ask_phone_number
from tgbot.keyboards.default.customer.who_are_you import who_are_you
from tgbot.keyboards.inline.customer.pagination import get_pages_keyboard
from tgbot.services.repository import Repo
from tgbot.states.customer.registration import RegistrationUser, RegistrationCourier


async def reg_starts(m: Message, state: FSMContext, referral=None,):  # @TODO регистрация рефералом
    await m.answer(text="Зарегистрироваться как <b>компания</b>, <b>частно е лицо</b> или <b>стать курьером</b>?",
                   reply_markup=who_are_you)
    await RegistrationUser.first()


# user
async def reg_type(m: Message, repo: Repo, state: FSMContext):
    if m.text == "👥 Компания":
        await state.update_data(type="Компания")
        await m.reply(text="Введите <b>название вашей компании</b>:", reply_markup=return_to_menu)
        await RegistrationUser.next()
    elif m.text == "👨‍💻 Частное лицо":
        await state.update_data(type='Частное лицо')
        await m.reply(text="🧑‍💼 Введите <b>ФИО</b>:", reply_markup=return_to_menu)
        await RegistrationUser.next()
    elif m.text == "🚚 Стать курьером":
        await m.reply(text="🧑‍💼 Введите <b>ФИО</b>:", reply_markup=return_to_menu)
        await RegistrationCourier.first()
    else:
        is_user_exists = await repo.is_customer_exists(user_id=m.chat.id)
        await m.answer(text="Главное меню", reply_markup=await user_main_menu(reg=is_user_exists))
        await state.finish()


async def reg_name(m: Message, repo: Repo, state: FSMContext):
    if m.text == "Вернуться в меню":
        is_user_exists = await repo.is_customer_exists(user_id=m.chat.id)
        await m.answer(text="Главное меню", reply_markup=await user_main_menu(reg=is_user_exists))
        await state.finish()
    else:
        async with state.proxy() as data:
            data['name'] = m.text

        cities_list = await repo.get_available_cities()
        if len(cities_list) > 0:
            await m.reply(text="📬 Выберите ваш город из списка",
                          reply_markup=await get_pages_keyboard(array=cities_list, width=2, items_per_page=10,
                                                                key="cities"))
            await RegistrationUser.next()
        else:
            await m.answer(text="В данный момент ни один город не активен. Регистрация будет сброшена.")
            await start(m, repo, state)


async def show_chosen_page(c: CallbackQuery, callback_data: dict, repo: Repo):
    cities_list = await repo.get_available_cities()
    current_page = int(callback_data.get("page"))

    try:
        await c.message.edit_reply_markup(
            await get_pages_keyboard(cities_list, width=2, items_per_page=10, page=current_page, key="cities"))
        await c.answer()
    except MessageNotModified:
        await c.answer(text="Страница не изменена")


async def set_city(c: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = callback_data['city_name'].lower()
        user_type = data['type']
    await c.answer(text=f"Выбран город {callback_data['city_name']}")
    if user_type == "Компания":
        await c.message.edit_text(text="📬 Введите <b>адрес компании</b>:")
    else:
        await c.message.edit_text(text="📬 Введите <b>ваш адрес</b>:\n"
                                       "<i>Например: Пушкина 20</i>")
    await RegistrationUser.next()


async def reg_address(m: Message, repo: Repo, state: FSMContext):
    if m.text == "Вернуться в меню":
        is_user_exists = await repo.is_customer_exists(user_id=m.chat.id)
        await m.answer(text="Главное меню", reply_markup=await user_main_menu(reg=is_user_exists))
        await state.finish()
    else:
        async with state.proxy() as data:
            data['address'] = m.text
            user_type = data['type']

        if user_type == "Компания":
            await m.reply(text="📱️ Введите <b>телефон компании</b>:",
                          reply_markup=return_to_menu)
        else:
            await m.reply(text="📱️ Введите <b>ваш номер телефона</b> или нажмите на <b>кнопку ниже</b>:",
                          reply_markup=ask_phone_number)
        await RegistrationUser.next()


async def reg_number(m: Message, repo: Repo, state: FSMContext):
    if m.text == "Вернуться в меню":
        is_user_exists = await repo.is_customer_exists(user_id=m.chat.id)
        await m.answer(text="Главное меню", reply_markup=await user_main_menu(reg=is_user_exists))
        await state.finish()
    else:
        if m.contact is not None:
            phone_number = m.contact.phone_number
        else:
            phone_number = m.text
        async with state.proxy() as data:
            data['number'] = phone_number

        await repo.add_customer(userid=m.chat.id, user_type=data['type'], name=data['name'],
                                city=data['city'], address=data['address'], number=data['number'])
        await state.finish()
        # await new_customer(m=m, customer_data=data, customer_id=customer_id) TODO логгинг
        await m.answer(text="👋 Вы зарегистрировались.\nТеперь вы можете оставить заказ!")
        await m.answer(text="Главное меню", reply_markup=await user_main_menu(reg=True))
