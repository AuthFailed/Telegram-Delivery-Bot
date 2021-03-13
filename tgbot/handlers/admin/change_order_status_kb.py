from aiogram.types import CallbackQuery

from tgbot.keyboards.inline.manager.order_status import change_order_status


async def change_order_status_kb(call: CallbackQuery, callback_data: dict):
    await call.answer()
    order_id = callback_data.get("order_id")
    await call.message.edit_reply_markup(reply_markup=await change_order_status(order_id=order_id))
