from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.keyboards.inline.manager.callback_data import order


async def order_keyboard(order_id: int):
    order_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⏳ Изменение статуса",
                    callback_data=order.new(item="change_status",
                                            order_id=order_id)
                )
            ],
            [
                InlineKeyboardButton(
                    text="📦 Выбор курьера",
                    callback_data=order.new(item="choose_courier",
                                            order_id=order_id)
                )
            ]
        ]
    )
    return order_kb
