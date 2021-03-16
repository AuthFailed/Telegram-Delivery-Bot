from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

broadcast = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text="✉️ Отправить"
            ),
            KeyboardButton(
                text="🔀 Другой пост"
            )
        ],
        [
            KeyboardButton(text="🏠 Вернуться в меню")
        ]
    ]
)
