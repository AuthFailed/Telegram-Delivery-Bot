from aiogram.dispatcher.filters.state import State, StatesGroup


class Order(StatesGroup):
    all_info = State()
    order_name = State()
    order_number = State()
    order_address = State()
    order_date = State()
    order_time = State()
    user_type = State()
    other_details = State()
    user_choice = State()
