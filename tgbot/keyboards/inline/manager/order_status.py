from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.manager.callback_data import order_status


async def change_order_status(order_id: int):
    change_status_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Заказ принят",
                    callback_data=order_status.new(order_id=order_id,
                                                   status="Заказ принят")
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📤 Курьер забрал заказ",
                    callback_data=order_status.new(order_id=order_id,
                                                   status="Курьер забрал заказ")
                )
            ],
            [
                InlineKeyboardButton(
                    text="📥 Курьер отдал заказ",
                    callback_data=order_status.new(order_id=order_id,
                                                   status="Курьер отдал заказ")
                )
            ],
            [
                InlineKeyboardButton(
                    text="✖️ Отмена заказа",
                    callback_data=order_status.new(order_id=order_id,
                                                   status="Отмена заказа")
                ),
                InlineKeyboardButton(
                    text="🏠 Вернуться",
                    callback_data=order_status.new(order_id=order_id,
                                                   status="Вернуться")
                )
            ],
        ]
    )
    return change_status_kb
