from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

personal_profile_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text="📦 Выполненные заказы"
            ),
            KeyboardButton(
                text="⏳ Сменить статус"
            )
        ],
        [
            KeyboardButton(
                text="🔨 Удалить профиль"
            )
        ],
        [
            KeyboardButton(
                text="🏠 Вернуться в меню"
            )
        ]
    ]
)
