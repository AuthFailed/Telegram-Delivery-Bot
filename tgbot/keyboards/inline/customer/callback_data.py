from aiogram.utils.callback_data import CallbackData

registration_city = CallbackData("reg_city", "city_name")
choose_order = CallbackData("order", "order_id")
calendar_callback = CallbackData('calendar', 'act', 'year', 'month', 'day')

pagination_call = CallbackData("paginator", "key", "page")
show_item_data = CallbackData("show_item", "item_id")

show_partner_data = CallbackData("show_partner", "partner_id")
show_manager_data = CallbackData("show_manager", "manager_id")
show_courier_data = CallbackData("show_courier", "courier_id")
