from aiogram.utils.callback_data import CallbackData

order = CallbackData("order", "item", "order_id")
order_status = CallbackData("order_status", "order_id", "status")
new_courier = CallbackData("courier", "courier_id", "status")
