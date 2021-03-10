from aiogram.dispatcher.filters.state import State, StatesGroup


class Registration(StatesGroup):
    user_type = State()
    name = State()
    address = State()
    number = State()
