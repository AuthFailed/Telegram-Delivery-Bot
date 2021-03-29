from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

choose_time = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text="8:00 - 10:00"
            ),
            KeyboardButton(
                text="10:00 - 12:00"
            )
        ],
        [
            KeyboardButton(
                text="12:00 - 14:00"
            ),
            KeyboardButton(
                text="14:00 - 16:00"
            )
        ],
        [
            KeyboardButton(
                text="16:00 - 18:00"
            ),
            KeyboardButton(
                text="18:00 - 20:00"
            )
        ],
        [
            KeyboardButton(
                text="20:00 - 22:00"
            ),
            KeyboardButton(
                text="22:00 - 24:00"
            )
        ],
        [
            KeyboardButton(
                text="🏠 Вернуться в меню"
            )
        ]
    ]
)
