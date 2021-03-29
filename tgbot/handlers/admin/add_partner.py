from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from tgbot.handlers.admin.manage_bot import manage_bot
from tgbot.handlers.admin.start import start
from tgbot.keyboards.default.admin.check_partner import check_partner
from tgbot.keyboards.default.admin.return_to_menu import return_to_menu
from tgbot.services import Repo
from tgbot.states.admin.new_partner import NewPartner


async def add_partner(m: Message, repo: Repo):
    admin_info = await repo.get_partner(admin_id=m.chat.id)
    if admin_info['ismain']:
        await m.answer(text="🏙️ Введите название города-партнера:",
                       reply_markup=return_to_menu)
        await NewPartner.first()
    else:
        await m.answer(text="У вас нет доступа к функционалу <b>главного администратора</b>!")


async def partner_city(m: Message, repo: Repo, state: FSMContext):
    is_city_exists = await repo.is_partner_exists(city=m.text.lower())
    if is_city_exists:
        await m.answer(text="🚫 Партнер с таким городом <b>уже существует</b> в базе данных.\n"
                            "Перейдите в меню управления партнерами для более подробной информации.")
        await state.finish()
        await manage_bot(m, repo)
        return
    await state.update_data(city=m.text.lower())
    await m.answer(text="👑 Введите ID администратора:",
                   reply_markup=return_to_menu)

    await NewPartner.next()


async def partner_id(m: Message, repo: Repo, state: FSMContext):
    if m.text.isdigit():
        is_partner_exists = await repo.is_partner_exists(partner_id=int(m.text))
        if is_partner_exists:
            await m.answer(text="🚫 Партнер с таким ID <b>уже существует</b> в базе данных.\n"
                                "Перейдите в меню управления партнерами для более подробной информации.")
            await state.finish()
            await manage_bot(m, repo)
            return
        await state.update_data(admin_id=m.text)
        partner_data = await state.get_data()
        await m.answer(text=f"""Проверьте введённые данные:
👑 ID администратора: <b>{partner_data['admin_id']}</b>
🏙 Город: <b>{partner_data['city'].title()}</b>
    """,
                       reply_markup=check_partner)
        await NewPartner.next()
    else:
        await m.answer(text="🚫 <b>Введите корректный ID</b>")


async def partner_choice(m: Message, repo: Repo, state: FSMContext):
    if m.text == "👌 Все правильно":
        partner_data = await state.get_data()
        await repo.add_partner(partner_id=partner_data['admin_id'],
                               city=partner_data['city'])
        await state.finish()
        await m.answer(text=f"""Вы успешно добавили нового партнера!
Подключенный город - <b>{partner_data['city'].title()}</b>.
Администратором назначен ID <b>{partner_data['admin_id']}</b>.
Отправьте партнеру (<a href="https://t.me/dostavka30rus_bot">ссылку на бота</a>) и попросите активировать его.""",
                       reply_markup=ReplyKeyboardRemove())
        await manage_bot(m, repo)
    elif m.text == "🔄 Заполнить заново":
        await state.finish()
        await m.answer(text="🏙️ Введите название города-партнера:", reply_markup=return_to_menu)
        await NewPartner.first()

    elif m.text == "🏠 Вернуться в меню":
        await start(m=m)
