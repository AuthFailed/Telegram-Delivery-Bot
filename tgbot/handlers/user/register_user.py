from aiogram import Dispatcher

from tgbot.handlers.user.change_user_data import change_user_data, user_choice, new_info
from tgbot.handlers.user.delete_profile import delete_profile, delete_profile_yes, delete_profile_no
from tgbot.handlers.user.order import order_starts, order_all_info, order_datetime, order_other_details, \
    order_user_choice
from tgbot.handlers.user.our_services import our_services
from tgbot.handlers.user.personal_profile import personal_profile
from tgbot.handlers.user.price_map import price_map
from tgbot.handlers.user.registration import *
from tgbot.handlers.user.start import *
from tgbot.handlers.user.tech_support import *
from tgbot.models.role import UserRole
from tgbot.states.user.change_user_info import ChangeUserInfo
from tgbot.states.user.delete_profile import DeleteProfile
from tgbot.states.user.order import Order


def register_user(dp: Dispatcher):
    # start
    dp.register_message_handler(user_start, commands=["start", "menu"], state="*", role=UserRole.USER)
    dp.register_message_handler(user_start, text="🏠 Вернуться в меню", state="*", role=UserRole.USER)

    # reg user
    dp.register_message_handler(reg_starts, text="✍️ Зарегистрироваться", role=UserRole.USER)
    dp.register_message_handler(reg_user_type, content_types=['text'], state=RegistrationUser.user_type)
    dp.register_message_handler(reg_user_name, content_types=['text'], state=RegistrationUser.name)
    dp.register_message_handler(reg_user_address, content_types=['text'], state=RegistrationUser.address)
    dp.register_message_handler(reg_user_number, content_types=['text'], state=RegistrationUser.number)

    # new order
    dp.register_message_handler(order_starts, text="🚩 Создать заказ", role=UserRole.USER)
    dp.register_message_handler(order_all_info, state=Order.all_info, role=UserRole.USER)
    dp.register_message_handler(order_datetime, state=Order.order_datetime, role=UserRole.USER)
    dp.register_message_handler(order_other_details, state=Order.other_details, role=UserRole.USER)
    dp.register_message_handler(order_user_choice, state=Order.user_choice, role=UserRole.USER)

    # user orders

    # personal profile
    dp.register_message_handler(personal_profile, text="👨‍💻 Личный кабинет", role=UserRole.USER)
    dp.register_message_handler(delete_profile, text="🔨 Удалить профиль", role=UserRole.USER)
    dp.register_message_handler(delete_profile_yes, text="✅ Да, я уверен(а)", state=DeleteProfile.user_choice)
    dp.register_message_handler(delete_profile_no, text="✖️ Нет, я передумал(а)", state=DeleteProfile.user_choice)
    dp.register_message_handler(change_user_data, text="📋 Изменить данные", role=UserRole.USER)
    dp.register_message_handler(user_choice, state=ChangeUserInfo.user_choice, role=UserRole.USER)
    dp.register_message_handler(new_info, state=ChangeUserInfo.new_info, role=UserRole.USER)

    # price map
    dp.register_message_handler(price_map, text="🗺️ Карта цен за доставку", role=UserRole.USER)

    # technical support
    dp.register_message_handler(tech_support, text="🙋 Тех. поддержка", role=UserRole.USER)

    # our services
    dp.register_message_handler(our_services, text="🚀 Наши услуги", role=UserRole.USER)
