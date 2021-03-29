from aiogram import Dispatcher
from aiogram.types import ChatType

from tgbot.handlers.groups.get_courier import get_courier
from tgbot.handlers.groups.get_customer import get_customer
from tgbot.handlers.groups.get_order import get_order
from tgbot.handlers.groups.set_city_group import set_orders_group, set_couriers_group, set_events_group
from tgbot.models.role import UserRole


def register_group(dp: Dispatcher):
    # Get courier info
    dp.register_message_handler(get_courier, commands=["курьер"], chat_type=[ChatType.SUPERGROUP, ChatType.GROUP],
                                role=[UserRole.MANAGER,
                                      UserRole.ADMIN])

    # Get order info
    dp.register_message_handler(get_order, commands=["заказ"], chat_type=[ChatType.SUPERGROUP, ChatType.GROUP],
                                role=[UserRole.MANAGER,
                                      UserRole.ADMIN])

    # Get customer new_info
    dp.register_message_handler(get_customer, commands=["заказчик"], chat_type=[ChatType.SUPERGROUP, ChatType.GROUP],
                                role=[UserRole.MANAGER,
                                      UserRole.ADMIN])

    dp.register_message_handler(set_orders_group, commands=["set_orders_group"],
                                chat_type=[ChatType.SUPERGROUP, ChatType.GROUP], is_admin=True)
    dp.register_message_handler(set_couriers_group, commands=["set_couriers_group"],
                                chat_type=[ChatType.SUPERGROUP, ChatType.GROUP], is_admin=True)
    dp.register_message_handler(set_events_group, commands=["set_events_group"],
                                chat_type=[ChatType.SUPERGROUP, ChatType.GROUP], is_admin=True)
