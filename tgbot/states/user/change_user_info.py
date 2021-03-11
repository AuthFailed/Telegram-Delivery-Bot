from aiogram.dispatcher.filters.state import State, StatesGroup


class ChangeUserInfo(StatesGroup):
    user_choice = State()
    new_info = State()
