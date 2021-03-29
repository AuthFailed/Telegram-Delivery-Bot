from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.default.customer.main_menu import main_menu
from tgbot.services.repository import Repo


async def start(m: Message, repo: Repo, state: FSMContext = None):
    if state is not None:
        await state.finish()
    is_user_exists = await repo.is_user_exists(user_id=m.chat.id)

    if is_user_exists:
        await m.answer(text="Главное меню",
                       reply_markup=await main_menu(reg=True))
    else:
        await m.answer(text=f"""Привет от MEGABOT.ДОСТАВКА!

Мы занимаемся доставкой различных товаров: <b>Цветы</b>, <b>Еда</b>, <b>Документы</b> и <b>многое другое</b>!
Работаем для компаний и частных лиц!
У нас есть Карта цен и круглосуточная служба поддержки!
Регистрируйся и создавай заказ уже сегодня!""",
                       parse_mode="html")
        await m.answer(
            text=f"Главное меню",
            reply_markup=await main_menu(reg=False)
        )
