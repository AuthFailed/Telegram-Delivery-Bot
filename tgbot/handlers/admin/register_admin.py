from aiogram import Dispatcher

from tgbot.handlers.admin import start


def register_admin(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start", "menu"])
