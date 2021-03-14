from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.manager.callback_data import choose_courier


async def choose_courier_kb(order_id: int, courier_list: list):
    keyboard = InlineKeyboardMarkup()
    for courier in courier_list:
        keyboard.add(InlineKeyboardButton(text=courier['name'],
                                          callback_data=choose_courier.new(order_id=order_id,
                                                                           courier_id=courier["userid"])))
    keyboard.add(InlineKeyboardButton(text="🏠 Вернуться", callback_data=choose_courier.new(courier_id="Вернуться",
                                                                                            order_id=order_id)))
    return keyboard
