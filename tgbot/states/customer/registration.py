from aiogram.dispatcher.filters.state import State, StatesGroup


class RegistrationUser(StatesGroup):
    type = State()
    name = State()
    city = State()
    address = State()
    number = State()


class RegistrationCourier(StatesGroup):
    name = State()
    city = State()
    number = State()
    passport_main = State()
    passport_registration = State()
    driving_license_front = State()
    driving_license_back = State()
