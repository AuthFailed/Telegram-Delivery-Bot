from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.admin.callback_data import courier


async def courier_kb(courier_data):
    markup = InlineKeyboardMarkup()
    if courier_data['applied'] is False:
        markup.add(InlineKeyboardButton(text="✅ Активировать",
                                        callback_data=courier.new(courier_id=courier_data['userid'],
                                                                  action="activate")))
    else:
        markup.add(InlineKeyboardButton(text="❌ Деактивировать",
                                        callback_data=courier.new(courier_id=courier_data['userid'],
                                                                  action="deactivate")))
    markup.add(InlineKeyboardButton(text="🗑️ Удалить партнера",
                                    callback_data=courier.new(courier_id=courier_data['userid'], action="delete")))
    markup.add(InlineKeyboardButton(text="🤝 К списку курьеров",
                                    callback_data=courier.new(courier_id="to_couriers", action="to_couriers")))
    return markup
