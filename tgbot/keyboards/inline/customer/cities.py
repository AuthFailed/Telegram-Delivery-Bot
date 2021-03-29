from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.customer.callback_data import registration_city


async def cities(cities_list):
    item_buttons = list()
    for city in cities_list:
        item_buttons.append(
            InlineKeyboardButton(
                text=city['city'].title(),
                callback_data=registration_city.new(city_name=city['city'])
            ))
    markup = InlineKeyboardMarkup()
    for button in item_buttons:
        markup.insert(button)
    return markup



