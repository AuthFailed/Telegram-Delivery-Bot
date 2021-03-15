from aiogram.dispatcher.filters.state import State, StatesGroup


class ChangeCourierStatus(StatesGroup):
    courier_choice = State()
