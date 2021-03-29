from aiogram.dispatcher.filters.state import State, StatesGroup


class NewPartner(StatesGroup):
    city = State()
    admin_id = State()
    choice = State()
