from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

change_status_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text="🛵 Свободен"
            ),
            KeyboardButton(
                text="🛵❗️ Занят"
            )
        ],
        [
            KeyboardButton(
                text="📦 На заказе"
            )
        ],
        [
            KeyboardButton(
                text="✖️ Отмена"
            ),
            KeyboardButton(
                text="🏠 Вернуться в меню"
            )
        ]
    ]
)
