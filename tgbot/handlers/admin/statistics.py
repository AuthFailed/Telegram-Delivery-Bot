from aiogram.types import Message


async def statistics(m: Message):  # @TODO сделать выбор типа статистики и добавить выбор периода
    await m.answer(text="👨‍💻 Этот раздел находится в разработке!")
