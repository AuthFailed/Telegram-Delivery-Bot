from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

check_courier = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text="👌 Все правильно"
            ),
            KeyboardButton(
                text="🔄 Заполнить заново"
            )
        ],
        [
            KeyboardButton(
                text="🏠 Вернуться в меню"
            )
        ]
    ]
)
