from aiogram import Dispatcher
from aiogram.types import ChatType, ContentTypes

from tgbot.handlers.courier.change_status import ask_for_status, set_new_status
from tgbot.handlers.courier.delete_profile import delete_profile, delete_profile_yes, delete_profile_no
from tgbot.handlers.courier.personal_profile import personal_profile
from tgbot.handlers.courier.registration import reg_name, reg_number, reg_passport_main, \
    reg_passport_registration, reg_driving_license_front, reg_driving_license_back
from tgbot.handlers.courier.start import start
from tgbot.handlers.courier.support_call import ask_support_call, send_to_support_call, answer_support_call, \
    not_supported, exit_support
from tgbot.keyboards.inline.manager.callback_data import support_callback, cancel_support_callback
from tgbot.models.role import UserRole
from tgbot.states.courier.change_status import ChangeStatus
from tgbot.states.courier.delete_profile import DeleteAccount
from tgbot.states.user.registration import RegistrationCourier


def register_courier(dp: Dispatcher):
    # start / menu
    dp.register_message_handler(start, commands=["start", "menu"], state="*", role=UserRole.COURIER,
                                chat_type=ChatType.PRIVATE)
    dp.register_message_handler(start, text="🏠 Вернуться в меню", state="*", role=UserRole.COURIER,
                                chat_type=ChatType.PRIVATE)

    # reg courier
    dp.register_message_handler(reg_name, content_types=['text'], state=RegistrationCourier.name,
                                chat_type=ChatType.PRIVATE)
    dp.register_message_handler(reg_number, content_types=['text'], state=RegistrationCourier.number,
                                chat_type=ChatType.PRIVATE)
    dp.register_message_handler(reg_passport_main, content_types=['photo'],
                                state=RegistrationCourier.passport_main,
                                chat_type=ChatType.PRIVATE)
    dp.register_message_handler(reg_passport_registration, content_types=['photo'],
                                state=RegistrationCourier.passport_registration,
                                chat_type=ChatType.PRIVATE)
    dp.register_message_handler(reg_driving_license_front, content_types=['photo'],
                                state=RegistrationCourier.driving_license_front,
                                chat_type=ChatType.PRIVATE)
    dp.register_message_handler(reg_driving_license_back, content_types=['photo'],
                                state=RegistrationCourier.driving_license_back,
                                chat_type=ChatType.PRIVATE)

    # personal info
    dp.register_message_handler(personal_profile, text="👨‍💻 Личный кабинет", role=UserRole.COURIER,
                                chat_type=ChatType.PRIVATE)
    dp.register_message_handler(ask_for_status, text="⏳ Сменить статус", role=UserRole.COURIER,
                                chat_type=ChatType.PRIVATE)
    dp.register_message_handler(set_new_status, content_types=['text'], state=ChangeStatus.courier_choice,
                                role=UserRole.COURIER,
                                chat_type=ChatType.PRIVATE)
    dp.register_message_handler(delete_profile, text="🔨 Удалить профиль", role=UserRole.COURIER,
                                chat_type=ChatType.PRIVATE)
    dp.register_message_handler(delete_profile_yes, text="✅ Да, я уверен(а)", state=DeleteAccount.choice,
                                chat_type=ChatType.PRIVATE)
    dp.register_message_handler(delete_profile_no, text="✖️ Нет, я передумал(а)",
                                state=DeleteAccount.choice,
                                chat_type=ChatType.PRIVATE)

    # Тех поддержка
    dp.register_message_handler(ask_support_call, text="🙋 Тех. поддержка", role=UserRole.COURIER,
                                chat_type=ChatType.PRIVATE)
    dp.register_callback_query_handler(send_to_support_call, support_callback.filter(messages="many", as_user="yes"),
                                       role=UserRole.COURIER, chat_type=ChatType.PRIVATE)
    dp.register_callback_query_handler(answer_support_call, support_callback.filter(messages="many", as_user="no"),
                                       role=UserRole.MANAGER, chat_type=ChatType.PRIVATE)
    dp.register_message_handler(not_supported, state="wait_in_support", content_types=ContentTypes.ANY,
                                role=UserRole.COURIER, chat_type=ChatType.PRIVATE)
    dp.register_callback_query_handler(exit_support, cancel_support_callback.filter(),
                                       state=["in_support", "wait_in_support", None])
