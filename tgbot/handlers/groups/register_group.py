from aiogram import Dispatcher
from aiogram.types import ChatType

from tgbot.handlers.groups.get_courier import get_courier
from tgbot.handlers.groups.get_order import get_order


def register_group(dp: Dispatcher):
    # Get courier info
    dp.register_message_handler(get_courier, commands=["курьер"], chat_type=ChatType.SUPERGROUP)

    # Get order info
    dp.register_message_handler(get_order, commands=["заказ"], chat_type=ChatType.SUPERGROUP)
