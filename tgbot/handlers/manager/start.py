from aiogram.dispatcher import FSMContext
from aiogram.types import Message


async def start(m: Message, state: FSMContext = None):
    if state is not None:
        await state.finish()

    await m.answer(text=f"Привет, <b>{m.from_user.full_name}</b>!")
