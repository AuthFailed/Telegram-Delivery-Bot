from aiogram.dispatcher import FSMContext
from aiogram.types import Message


async def start(m: Message, state: FSMContext = None):
    if state is not None:
        await state.finish()

    await m.answer(text=f"Привет, <b>менеджер</b>!\n"
                        f"У тебя пока нет личного меню, но есть пара команд: /заказчик, /заказ и /курьер")
