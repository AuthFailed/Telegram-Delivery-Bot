from aiogram.dispatcher.filters.state import State, StatesGroup


class NewManager(StatesGroup):
    manager_id = State()
    fio = State()
    number = State()
    choice = State()
