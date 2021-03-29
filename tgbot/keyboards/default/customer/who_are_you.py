from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

who_are_you = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text="👥 Компания"
            ),
            KeyboardButton(
                text="👨‍💻 Частное лицо"
            )
        ],
        [
            KeyboardButton(
                text="🚚 Стать курьером"
            )
        ],
        [
            KeyboardButton(
                text="🏠 Вернуться в меню"
            )
        ]
    ]
)
