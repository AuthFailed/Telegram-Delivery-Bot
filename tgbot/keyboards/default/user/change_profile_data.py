from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def change_profile_data(user_type: str):
    if user_type == "Компания":
        keyboard = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(
                        text="👥 Название компании"
                    )
                ],
                [
                    KeyboardButton(
                        text="📬 Адрес"
                    ),
                    KeyboardButton(
                        text="☎️ Номер"
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
    else:
        keyboard = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(
                        text="👤 ФИО"
                    )
                ],
                [
                    KeyboardButton(
                        text="📬 Адрес"
                    ),
                    KeyboardButton(
                        text="☎️ Номер"
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
    return keyboard
