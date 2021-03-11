from aiogram.dispatcher.filters.state import State, StatesGroup


class RegistrationUser(StatesGroup):
    user_type = State()
    name = State()
    address = State()
    number = State()


class RegistrationCourier(StatesGroup):
    name = State()
    number = State()
    passport_main = State()
    passport_registration = State()
    driving_license_front = State()
    driving_license_back = State()
