from aiogram.dispatcher.filters.state import State, StatesGroup


class NewCourier(StatesGroup):
    id = State()
    name = State()
    number = State()
    passport_main = State()
    passport_registration = State()
    driving_license_front = State()
    driving_license_back = State()
    choice = State()
