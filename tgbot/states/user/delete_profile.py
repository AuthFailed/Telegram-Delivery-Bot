from aiogram.dispatcher.filters.state import State, StatesGroup


class DeleteProfile(StatesGroup):
    user_choice = State()
