from aiogram.dispatcher.filters.state import State, StatesGroup


class DeleteProfile(StatesGroup):
    choice = State()
