from aiogram.utils.callback_data import CallbackData

order = CallbackData("order", "item", "order_id")
order_status = CallbackData("order_status", "order_id", "status")

new_courier = CallbackData("courier", "courier_id", "status")
choose_courier = CallbackData("choose_courier", "order_id", "courier_id")

support_callback = CallbackData("ask_support", "messages", "user_id", "as_user")
cancel_support_callback = CallbackData("cancel_support", "user_id")
