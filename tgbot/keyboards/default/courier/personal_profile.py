from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

personal_profile_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text="📦 Мои заказы"
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
