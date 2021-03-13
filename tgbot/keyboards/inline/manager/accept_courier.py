from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.manager.callback_data import new_courier


async def courier_request_kb(courier_id: int):
    courier_request = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👌 Принять заявку",
                    callback_data=new_courier.new(courier_id=courier_id, status=True)
                )
            ],
            [
                InlineKeyboardButton(
                    text="✖️ Отклонить заявку",
                    callback_data=new_courier.new(courier_id=courier_id, status=False)
                )
            ]
        ]
    )
    return courier_request
