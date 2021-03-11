from aiogram import Dispatcher

from tgbot.handlers.courier.start import courier_start
from tgbot.models.role import UserRole


def register_courier(dp: Dispatcher):
    # start / menu
    dp.register_message_handler(courier_start, commands=["start", "menu"], state="*", role=UserRole.COURIER)
    dp.register_message_handler(courier_start, text="🏠 Вернуться в меню", state="*", role=UserRole.COURIER)
