from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def manage_bot_kb(is_main: bool):
    if is_main:
        keyboard = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(
                        text="📢 Рассылка"
                    )
                ],
                [
                    KeyboardButton(text="🤝 Партнеры"),
                    KeyboardButton(text="👨‍💼 Менеджеры"),
                    KeyboardButton(text="🚚 Курьеры")
                ],
                [
                    KeyboardButton(
                        text="⚙️ Статус сервера"
                    )
                ],
                [
                    KeyboardButton(
                        text="🏠 Вернуться в меню"
                    )
                ]
            ]
        )
    else:
        keyboard = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(
                        text="📢 Рассылка"
                    )
                ],
                [
                    KeyboardButton(text="👨‍💼 Менеджеры"),
                    KeyboardButton(text="🚚 Курьеры")
                ],
                [
                    KeyboardButton(
                        text="⚙️ Статус сервера"
                    )
                ],
                [
                    KeyboardButton(
                        text="🏠 Вернуться в меню"
                    )
                ]
            ]
        )
    return keyboard
