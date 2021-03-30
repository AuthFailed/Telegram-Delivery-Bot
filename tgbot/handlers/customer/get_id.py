from aiogram.types import Message


async def get_my_id(m: Message):
    await m.answer(f"""
Ваш ID: <code>{m.from_user.id}</code>""")
