from aiogram import Dispatcher

from tgbot.handlers.manager.change_courier_apply_status import change_courier_apply_status
from tgbot.handlers.manager.order_interaction import change_order_status_kb, change_order_status_db, \
    list_of_available_couriers, set_order_courier, update_order_info
from tgbot.keyboards.inline.manager.callback_data import order, order_status, new_courier, choose_courier


def register_manager(dp: Dispatcher):
    # order
    dp.register_callback_query_handler(change_order_status_kb, order.filter(item="change_status"))
    dp.register_callback_query_handler(list_of_available_couriers, order.filter(item="choose_courier"))
    dp.register_callback_query_handler(update_order_info, order.filter(item="update_info"))
    dp.register_callback_query_handler(change_order_status_db, order_status.filter())
    dp.register_callback_query_handler(set_order_courier, choose_courier.filter())

    # new courier registered
    dp.register_callback_query_handler(change_courier_apply_status, new_courier.filter())
