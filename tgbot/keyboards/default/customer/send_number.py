from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

ask_phone_number = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text="📱 Отправить телефон",
                request_contact=True
            )
        ],
        [
            KeyboardButton(
                text="🏠 Вернуться в меню"
            )
        ]
    ]
)
