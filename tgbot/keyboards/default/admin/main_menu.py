from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="📈 Статистика"
            )
        ],
        [
            KeyboardButton(
                text='🚚 Управление курьерами'
            )
        ],
        [
            KeyboardButton(
                text='🤖 Управление ботом'
            )
        ]
    ],
    resize_keyboard=True
)
