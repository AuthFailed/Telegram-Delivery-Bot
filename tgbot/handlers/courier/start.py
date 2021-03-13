from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.default.courier.main_menu import main_menu


async def courier_start(m: Message, state: FSMContext = None):
    if state is not None:
        await state.finish()

    await m.answer(text="Главное меню",
                   reply_markup=main_menu)
