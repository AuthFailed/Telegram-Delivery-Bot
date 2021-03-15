from aiogram.dispatcher.filters.state import State, StatesGroup


class ChangeStatus(StatesGroup):
    courier_choice = State()
