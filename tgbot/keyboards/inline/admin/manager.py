from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.admin.callback_data import manager


async def manager_kb(manager_data):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="🗑️ Удалить менеджера", callback_data=manager.new(manager_id=manager_data['userid'], action="delete")))
    markup.add(InlineKeyboardButton(text="👨‍💼 К списку менеджеров", callback_data=manager.new(manager_id="to_managers", action="to_managers")))
    return markup
