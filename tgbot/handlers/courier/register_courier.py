from aiogram import Dispatcher

from tgbot.handlers.courier.personal_profile import personal_profile
from tgbot.handlers.courier.registration import reg_courier_name, reg_courier_number, reg_courier_passport_main, \
    reg_courier_passport_registration, reg_courier_driving_license_front, reg_courier_driving_license_back
from tgbot.handlers.courier.start import courier_start
from tgbot.models.role import UserRole
from tgbot.states.user.registration import RegistrationCourier


def register_courier(dp: Dispatcher):
    # start / menu
    dp.register_message_handler(courier_start, commands=["start", "menu"], state="*", role=UserRole.COURIER)
    dp.register_message_handler(courier_start, text="🏠 Вернуться в меню", state="*", role=UserRole.COURIER)

    # reg courier
    dp.register_message_handler(reg_courier_name, content_types=['text'], state=RegistrationCourier.name)
    dp.register_message_handler(reg_courier_number, content_types=['text'], state=RegistrationCourier.number)
    dp.register_message_handler(reg_courier_passport_main, content_types=['photo'],
                                state=RegistrationCourier.passport_main)
    dp.register_message_handler(reg_courier_passport_registration, content_types=['photo'],
                                state=RegistrationCourier.passport_registration)
    dp.register_message_handler(reg_courier_driving_license_front, content_types=['photo'],
                                state=RegistrationCourier.driving_license_front)
    dp.register_message_handler(reg_courier_driving_license_back, content_types=['photo'],
                                state=RegistrationCourier.driving_license_back)
    # personal info
    dp.register_message_handler(personal_profile, text="👨‍💻 Личный кабинет", state="*", role=UserRole.COURIER)
