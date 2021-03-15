from aiogram import Dispatcher, types

from tgbot.handlers.courier.change_status import ask_for_status, set_new_status
from tgbot.handlers.courier.delete_profile import delete_profile, delete_profile_yes, delete_profile_no
from tgbot.handlers.courier.personal_profile import personal_profile
from tgbot.handlers.courier.registration import reg_name, reg_number, reg_passport_main, \
    reg_passport_registration, reg_driving_license_front, reg_driving_license_back
from tgbot.handlers.courier.start import start
from tgbot.models.role import UserRole
from tgbot.states.courier.change_status import ChangeStatus
from tgbot.states.courier.delete_profile import DeleteAccount
from tgbot.states.user.registration import RegistrationCourier


def register_courier(dp: Dispatcher):
    # start / menu
    dp.register_message_handler(start, commands=["start", "menu"], state="*", role=UserRole.COURIER,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(start, text="🏠 Вернуться в меню", state="*", role=UserRole.COURIER,
                                chat_type=types.ChatType.PRIVATE)

    # reg courier
    dp.register_message_handler(reg_name, content_types=['text'], state=RegistrationCourier.name,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(reg_number, content_types=['text'], state=RegistrationCourier.number,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(reg_passport_main, content_types=['photo'],
                                state=RegistrationCourier.passport_main,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(reg_passport_registration, content_types=['photo'],
                                state=RegistrationCourier.passport_registration,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(reg_driving_license_front, content_types=['photo'],
                                state=RegistrationCourier.driving_license_front,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(reg_driving_license_back, content_types=['photo'],
                                state=RegistrationCourier.driving_license_back,
                                chat_type=types.ChatType.PRIVATE)

    # personal info
    dp.register_message_handler(personal_profile, text="👨‍💻 Личный кабинет", role=UserRole.COURIER,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(ask_for_status, text="⏳ Сменить статус", role=UserRole.COURIER,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(set_new_status, content_types=['text'], state=ChangeStatus.courier_choice,
                                role=UserRole.COURIER,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(delete_profile, text="🔨 Удалить профиль", role=UserRole.COURIER,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(delete_profile_yes, text="✅ Да, я уверен(а)", state=DeleteAccount.choice,
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(delete_profile_no, text="✖️ Нет, я передумал(а)",
                                state=DeleteAccount.choice,
                                chat_type=types.ChatType.PRIVATE)
