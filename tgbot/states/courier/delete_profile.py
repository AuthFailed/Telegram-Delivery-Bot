from aiogram.dispatcher.filters.state import State, StatesGroup


class DeleteCourierAccount(StatesGroup):
    courier_choice = State()
