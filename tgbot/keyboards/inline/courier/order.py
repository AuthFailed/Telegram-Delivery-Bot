from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.keyboards.inline.manager.callback_data import order


async def courier_order_keyboard_kb(order_id: int):
    keyboard = InlineKeyboardMarkup(
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
                    text="🔄 Обновить",
                    callback_data=order.new(item="update_info",
                                            order_id=order_id)
                )
            ],
            [
                InlineKeyboardButton(
                    text="👨‍💼 Связаться с менеджером",
                    callback_data=order.new(item="contact_with_manager",
                                            order_id=order_id)
                )
            ]
        ]
    )
    return keyboard
