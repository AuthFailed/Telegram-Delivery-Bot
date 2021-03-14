from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def main_menu(reg: bool):
    if reg:
        keyboard = ReplyKeyboardMarkup(row_width=1,
                                       resize_keyboard=True,
                                       keyboard=[
                                           [
                                               KeyboardButton(
                                                   text="🚩 Создать заказ"
                                               ),
                                               KeyboardButton(
                                                   text="👨‍💻 Личный кабинет"
                                               )
                                           ],
                                           [
                                               KeyboardButton(
                                                   text="🗺️ Карта цен за доставку"  # url="https://goo.su/3yKr"
                                               )
                                           ],
                                           [
                                               KeyboardButton(
                                                   text="🚀 Наши услуги"
                                               ),
                                               KeyboardButton(
                                                   text="🙋 Тех. поддержка"
                                               )
                                           ]
                                       ])
    else:
        keyboard = ReplyKeyboardMarkup(row_width=1,
                                       resize_keyboard=True,
                                       keyboard=[
                                           [
                                               KeyboardButton(
                                                   text="✍️ Зарегистрироваться"
                                               )
                                           ],
                                           [
                                               KeyboardButton(
                                                   text="🗺️ Карта цен за доставку"  # url="https://goo.su/3yKr"
                                               )
                                           ],
                                           [
                                               KeyboardButton(
                                                   text="🚀 Наши услуги"
                                               ),
                                               KeyboardButton(
                                                   text="🙋 Тех. поддержка"
                                               )
                                           ]
                                       ])
    return keyboard
