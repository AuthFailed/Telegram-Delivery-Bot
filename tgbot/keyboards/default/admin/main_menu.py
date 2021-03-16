from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
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
    ]
)
