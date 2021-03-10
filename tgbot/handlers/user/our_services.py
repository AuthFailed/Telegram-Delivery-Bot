from aiogram.types import Message

from tgbot.keyboards.default.user.return_to_menu import return_to_menu


async def our_services(m: Message):
    await m.answer_photo(photo="https://i.imgur.com/H9zCB4f.jpg",
                         reply_markup=return_to_menu)
