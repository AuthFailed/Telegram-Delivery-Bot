from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def change_user_info(user_type: str):
    if user_type == "Компания":
        change_user_info_kb = ReplyKeyboardMarkup(
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
        change_user_info_kb = ReplyKeyboardMarkup(
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
    return change_user_info_kb
