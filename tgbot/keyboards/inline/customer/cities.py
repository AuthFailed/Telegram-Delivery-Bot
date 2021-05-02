from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.customer.callback_data import registration_city


async def available_cities(cities_list: list):
    keyboard = InlineKeyboardMarkup()
    for city in cities_list:
        keyboard.add(InlineKeyboardButton(text=f"{city['city']}",
                                          callback_data=registration_city.new(city_name=city['city'])))
    return keyboard
