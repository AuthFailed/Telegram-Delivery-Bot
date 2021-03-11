from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

manage_couriers = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text="Список курьеров"
            )
        ],
        [
            KeyboardButton(
                text="Вернуться в меню"
            )
        ]
    ]
)
