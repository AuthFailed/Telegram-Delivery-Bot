from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.admin.callback_data import partner


async def partner_kb(partner_data):
    markup = InlineKeyboardMarkup()
    if partner_data['isworking'] is False:
        markup.add(InlineKeyboardButton(text="✅ Активировать",
                                        callback_data=partner.new(partner_id=partner_data['adminid'], action="activate")))
    else:
        markup.add(InlineKeyboardButton(text="❌ Деактивировать",
                                        callback_data=partner.new(partner_id=partner_data['adminid'],
                                                                  action="deactivate")))
    markup.add(InlineKeyboardButton(text="🗑️ Удалить партнера", callback_data=partner.new(partner_id=partner_data['adminid'], action="delete")))
    markup.add(InlineKeyboardButton(text="🤝 К списку партнеров", callback_data=partner.new(partner_id="to_partners", action="to_partners")))
    return markup
