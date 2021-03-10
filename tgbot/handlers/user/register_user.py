from aiogram import Dispatcher

from tgbot.handlers.user.order import order_starts, order_all_info, order_datetime, order_other_details, \
    order_user_choice
from tgbot.handlers.user.our_services import our_services
from tgbot.handlers.user.personal_profile import personal_profile
from tgbot.handlers.user.price_map import price_map
from tgbot.handlers.user.registration import *
from tgbot.handlers.user.start import *
from tgbot.handlers.user.tech_support import *
from tgbot.models.role import UserRole
from tgbot.states.user.order import Order
from tgbot.states.user.registration import Registration


def register_user(dp: Dispatcher):
    # start
    dp.register_message_handler(user_start, commands=["start", "menu"], state="*")
    dp.register_message_handler(user_start, text="🏠 Вернуться в меню", state="*")

    # registration
    dp.register_message_handler(reg_starts, text="✍️ Зарегистрироваться", role=UserRole.USER)
    dp.register_message_handler(reg_user_type, content_types=['text'], state=Registration.user_type, role=UserRole.USER)
    dp.register_message_handler(reg_name, content_types=['text'], state=Registration.name, role=UserRole.USER)
    dp.register_message_handler(reg_address, content_types=['text'], state=Registration.address, role=UserRole.USER)
    dp.register_message_handler(reg_number, content_types=['text'], state=Registration.number, role=UserRole.USER)

    # new order
    dp.register_message_handler(order_starts, text="🚩 Создать заявку")
    dp.register_message_handler(order_all_info, state=Order.all_info)
    dp.register_message_handler(order_datetime, state=Order.order_datetime)
    dp.register_message_handler(order_other_details, state=Order.other_details)
    dp.register_message_handler(order_user_choice, state=Order.user_choice)

    # user orders

    # personal profile
    dp.register_message_handler(personal_profile, text="👨‍💻 Личный кабинет")

    # price map
    dp.register_message_handler(price_map, text="🗺️ Карта цен за доставку")

    # technical support
    dp.register_message_handler(tech_support, text="🙋 Тех. поддержка")

    # our services
    dp.register_message_handler(our_services, text="🚀 Наши услуги")
