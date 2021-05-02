from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.customer.callback_data import choose_order


async def my_orders_kb(user_orders: list):
    keyboard = InlineKeyboardMarkup()
    for order in user_orders:
        keyboard.add(InlineKeyboardButton(text=f"Заказ №{order['id']} | {order['status']}",
                                          callback_data=choose_order.new(order_id=order['id'])))
    return keyboard
