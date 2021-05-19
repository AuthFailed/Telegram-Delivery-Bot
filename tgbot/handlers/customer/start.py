from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.default.customer.main_menu import main_menu
from tgbot.keyboards.default.customer.who_are_you import who_are_you
from tgbot.services.repository import Repo
from tgbot.states.customer.registration import RegistrationUser


async def start(m: Message, repo: Repo, state: FSMContext = None):
    referral = m.get_args()
    if state is not None:
        await state.finish()
    is_user_exists = await repo.is_customer_exists(user_id=m.chat.id)

    if is_user_exists:
        await m.answer(text="Главное меню",
                       reply_markup=await main_menu(reg=True))
    else:
        if referral == "" or referral is None:
            await m.answer(text=f"""Привет от MEGABOT.ДОСТАВКА!

Мы занимаемся доставкой различных товаров: <b>Цветы</b>, <b>Еда</b>, <b>Документы</b> и <b>многое другое</b>!
Работаем для компаний и частных лиц!
У нас есть Карта цен и круглосуточная служба поддержки!
Регистрируйся и создавай заказ уже сегодня!""",
                           parse_mode="html")
            await m.answer(
                text=f"Главное меню",
                reply_markup=await main_menu(reg=is_user_exists)
            )
        else:
            await RegistrationUser.first()
            await m.answer(text=f"""Привет от MEGABOT.ДОСТАВКА!

Мы занимаемся доставкой различных товаров: <b>Цветы</b>, <b>Еда</b>, <b>Документы</b> и <b>многое другое</b>!
Работаем для компаний и частных лиц!

Вас пригласил {referral}""")
            await m.answer(
                    text="Зарегистрироваться как <b>компания</b>, <b>частно е лицо</b> или <b>стать курьером</b>?",
                    reply_markup=who_are_you)
