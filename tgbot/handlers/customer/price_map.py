from aiogram.types import Message

from tgbot.keyboards.default.user.return_to_menu import return_to_menu


async def price_map(m: Message):
    await m.answer(text="🗺️ Карта цен за доставку:\n"
                        "https://goo.su/3yKr",
                   reply_markup=return_to_menu)
