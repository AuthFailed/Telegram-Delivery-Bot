from aiogram import Dispatcher

from tgbot.handlers.admin.change_order_status import change_order_status_db
from tgbot.handlers.admin.change_order_status_kb import change_order_status_kb
from tgbot.handlers.admin.start import admin_start
from tgbot.keyboards.inline.admin.callback_data import order, order_status
from tgbot.models.role import UserRole


def register_admin(dp: Dispatcher):
    # start / menu
    dp.register_message_handler(admin_start, commands=["start", "menu"], state="*", role=UserRole.ADMIN)
    dp.register_message_handler(admin_start, text="🏠 Вернуться в меню", state="*", role=UserRole.ADMIN)

    # order
    dp.register_callback_query_handler(change_order_status_kb, order.filter(item="change_status"))
    dp.register_callback_query_handler(change_order_status_db, order_status.filter())
