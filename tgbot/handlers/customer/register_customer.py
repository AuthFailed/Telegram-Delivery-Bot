from aiogram import Dispatcher, types

from tgbot.handlers.customer.change_customer__data import change_user_data, user_choice, new_info
from tgbot.handlers.customer.delete_profile import delete_profile, delete_profile_yes, delete_profile_no
from tgbot.handlers.customer.order import order_starts, order_all_info, order_time, order_other_details, \
    order_user_choice, order_date
from tgbot.handlers.customer.orders_interaction import list_of_available_orders, get_order_info
from tgbot.handlers.customer.our_services import our_services
from tgbot.handlers.customer.personal_profile import personal_profile
from tgbot.handlers.customer.price_map import price_map
from tgbot.handlers.customer.registration import *
from tgbot.handlers.customer.start import *
from tgbot.handlers.customer.tech_support import *
from tgbot.keyboards.inline.customer.callback_data import calendar_callback
from tgbot.keyboards.inline.customer.callback_data import choose_order
from tgbot.models.role import UserRole
from tgbot.states.user.change_user_info import ChangeUserInfo
from tgbot.states.user.delete_profile import DeleteProfile
from tgbot.states.user.order import Order


def register_customer(dp: Dispatcher):
    # start
    dp.register_message_handler(user_start, commands=["start", "menu"], state="*", role=UserRole.USER,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(user_start, text="🏠 Вернуться в меню", state="*", role=UserRole.USER,
                                chat_type=types.ChatType.PRIVATE)

    # reg user
    dp.register_message_handler(reg_starts, text="✍️ Зарегистрироваться", role=UserRole.USER,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(reg_user_type, content_types=['text'], state=RegistrationUser.user_type,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(reg_user_name, content_types=['text'], state=RegistrationUser.name,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(reg_user_address, content_types=['text'], state=RegistrationUser.address,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(reg_user_number, content_types=['text'], state=RegistrationUser.number,
                                chat_type=types.ChatType.PRIVATE)

    # new order
    dp.register_message_handler(order_starts, text="🚩 Создать заказ", role=UserRole.USER,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(order_all_info, state=Order.all_info, role=UserRole.USER,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_callback_query_handler(order_date, calendar_callback.filter(), state=Order.order_date,
                                       role=UserRole.USER,
                                       chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(order_time, state=Order.order_time, role=UserRole.USER,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(order_other_details, state=Order.other_details, role=UserRole.USER,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(order_user_choice, state=Order.user_choice, role=UserRole.USER,
                                chat_type=types.ChatType.PRIVATE)

    # user orders

    # personal profile
    dp.register_message_handler(personal_profile, text="👨‍💻 Личный кабинет", role=UserRole.USER,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(list_of_available_orders, text="📦 Мои заказы", role=UserRole.USER)
    dp.register_callback_query_handler(get_order_info, choose_order.filter())
    dp.register_message_handler(change_user_data, text="📋 Изменить данные", role=UserRole.USER,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(delete_profile, text="🔨 Удалить профиль", role=UserRole.USER,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(delete_profile_yes, text="✅ Да, я уверен(а)", state=DeleteProfile.user_choice,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(delete_profile_no, text="✖️ Нет, я передумал(а)", state=DeleteProfile.user_choice,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(user_choice, state=ChangeUserInfo.user_choice, role=UserRole.USER,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(new_info, state=ChangeUserInfo.new_info, role=UserRole.USER,
                                chat_type=types.ChatType.PRIVATE)

    # price map
    dp.register_message_handler(price_map, text="🗺️ Карта цен за доставку", role=UserRole.USER,
                                chat_type=types.ChatType.PRIVATE)

    # technical support
    dp.register_message_handler(tech_support, text="🙋 Тех. поддержка", role=UserRole.USER,
                                chat_type=types.ChatType.PRIVATE)

    # our services
    dp.register_message_handler(our_services, text="🚀 Наши услуги", role=UserRole.USER,
                                chat_type=types.ChatType.PRIVATE)
