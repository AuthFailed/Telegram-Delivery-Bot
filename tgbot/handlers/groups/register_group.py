from aiogram import Dispatcher
from aiogram.types import ChatType

from tgbot.handlers.groups.get_courier import get_courier
from tgbot.handlers.groups.get_customer import get_customer
from tgbot.handlers.groups.get_order import get_order
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
