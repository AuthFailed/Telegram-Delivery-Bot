from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text="📢 Рассылка"
            )
        ],
        [
            KeyboardButton(
                text="⚙️ Статус сервера"
            )
        ],
        [
            KeyboardButton(
                text="🏠 Вернуться в меню"
            )
        ]
    ]
)
