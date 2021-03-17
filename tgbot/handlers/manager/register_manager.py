from aiogram import Dispatcher
from aiogram.types import ChatType

from tgbot.handlers.manager.change_courier_apply_status import change_courier_apply_status
from tgbot.handlers.manager.get_courier import get_courier
from tgbot.handlers.manager.get_customer import get_customer
from tgbot.handlers.manager.get_order import get_order
from tgbot.handlers.manager.order_interaction import change_order_status_kb, change_order_status_db, \
    list_of_available_couriers, set_order_courier, update_order_info, current_page_error
from tgbot.handlers.manager.start import start
from tgbot.keyboards.inline.customer.callback_data import pagination_call
from tgbot.keyboards.inline.manager.callback_data import order, order_status, new_courier, choose_courier
from tgbot.models.role import UserRole


def register_manager(dp: Dispatcher):
    # start
    dp.register_message_handler(start, commands=["start", "menu"], state="*", role=UserRole.MANAGER,
                                chat_type=ChatType.PRIVATE)

    # order
    dp.register_callback_query_handler(change_order_status_kb, order.filter(item="change_status"),
                                       role=[UserRole.MANAGER,
                                       UserRole.ADMIN])
    dp.register_callback_query_handler(list_of_available_couriers, order.filter(item="choose_courier"),
                                       role=[UserRole.MANAGER,
                                       UserRole.ADMIN])
    dp.register_callback_query_handler(update_order_info, order.filter(item="update_info"), role=[UserRole.MANAGER,
                                       UserRole.ADMIN])
    dp.register_callback_query_handler(change_order_status_db, order_status.filter(), role=[UserRole.MANAGER,
                                       UserRole.ADMIN])
    dp.register_callback_query_handler(set_order_courier, choose_courier.filter(), role=[UserRole.MANAGER,
                                       UserRole.ADMIN])

    dp.register_callback_query_handler(current_page_error, pagination_call.filter(page="current_page"))


    # new courier registered
    dp.register_callback_query_handler(change_courier_apply_status, new_courier.filter(), role=[UserRole.MANAGER,
                                       UserRole.ADMIN])

    dp.register_message_handler(get_courier, commands=["курьер"], chat_type=ChatType.PRIVATE, role=UserRole.MANAGER)

    # Get order info
    dp.register_message_handler(get_order, commands=["заказ"], chat_type=ChatType.PRIVATE, role=UserRole.MANAGER)

    # Get customer new_info
    dp.register_message_handler(get_customer, commands=["заказчик"], chat_type=ChatType.PRIVATE,
                                role=UserRole.MANAGER)
