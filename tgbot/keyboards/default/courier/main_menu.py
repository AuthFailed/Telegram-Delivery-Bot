from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="👨‍💻 Личный кабинет"
            )
        ],
        [
            KeyboardButton(
                text='🙋 Тех. поддержка'
            )
        ]
    ],
    resize_keyboard=True
)
