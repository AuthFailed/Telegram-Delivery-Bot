from aiogram import Dispatcher
from aiogram.types import ChatType

from tgbot.handlers.groups.set_city_group import set_orders_group, set_couriers_group, set_events_group


def register_group(dp: Dispatcher):
    dp.register_message_handler(set_orders_group, commands=["set_orders_group"],
                                chat_type=[ChatType.SUPERGROUP, ChatType.GROUP], is_admin=True)
    dp.register_message_handler(set_couriers_group, commands=["set_couriers_group"],
                                chat_type=[ChatType.SUPERGROUP, ChatType.GROUP], is_admin=True)
    dp.register_message_handler(set_events_group, commands=["set_events_group"],
                                chat_type=[ChatType.SUPERGROUP, ChatType.GROUP], is_admin=True)
