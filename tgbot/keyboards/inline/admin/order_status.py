from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.admin.callback_data import order_status


async def change_order_status(order_id: int):
    change_status_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Заявка принята",
                    callback_data=order_status.new(order_id=order_id,
                                                   status="Заявка принята")
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Курьер забрал заказ",
                    callback_data=order_status.new(order_id=order_id,
                                                   status="Курьер забрал заказ")
                )
            ],
            [
                InlineKeyboardButton(
                    text="Курьер отдал заказ",
                    callback_data=order_status.new(order_id=order_id,
                                                   status="Курьер отдал заказ")
                )
            ],
            [
                InlineKeyboardButton(
                    text="Отмена заявки",
                    callback_data=order_status.new(order_id=order_id,
                                                   status="Отмена заявки")
                )
            ]
        ]
    )
    return change_status_kb
