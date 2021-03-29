from aiogram.dispatcher.filters.state import State, StatesGroup


class DeleteAccount(StatesGroup):
    choice = State()
