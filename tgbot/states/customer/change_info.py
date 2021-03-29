from aiogram.dispatcher.filters.state import State, StatesGroup


class ChangeInfo(StatesGroup):
    choice = State()
    new_info = State()
