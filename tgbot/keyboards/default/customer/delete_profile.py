from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

delete_profile_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text="✅ Да, я уверен(а)"
            ),
            KeyboardButton(
                text="✖️ Нет, я передумал(а)"
            )
        ],
        [
            KeyboardButton(
                text="🏠 Вернуться в меню"
            )
        ]
    ]
)
