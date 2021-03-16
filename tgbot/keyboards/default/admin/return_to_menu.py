from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

return_to_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text="🏠 Вернуться в меню"
            )
        ]
    ]
)
