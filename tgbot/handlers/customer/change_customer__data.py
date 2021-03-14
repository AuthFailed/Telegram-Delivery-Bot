from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.handlers.customer.personal_profile import personal_profile
from tgbot.keyboards.default.user.change_user_info import change_user_info
from tgbot.keyboards.default.user.return_to_menu import return_to_menu
from tgbot.services.event_handlers import customer_changed_profile_data
from tgbot.services.repository import Repo
from tgbot.states.user.change_user_info import ChangeUserInfo


async def change_user_data(m: Message, repo: Repo):
    user = await repo.get_user(user_id=m.chat.id)
    await m.reply(text="🖊️ Выберите, какую информацию вы хотите изменить:",
                  reply_markup=await change_user_info(user_type=user['usertype']))
    await ChangeUserInfo.first()


async def user_choice(m: Message, repo: Repo, state: FSMContext):
    if m.text == "👥 Название компании":
        await state.update_data(user_choice="name")
        await m.reply("👥 Введите новое название компании:", reply_markup=return_to_menu)
        await ChangeUserInfo.next()
    elif m.text == "👤 ФИО":
        await state.update_data(user_choice="name")
        await m.reply("👥 Введите ФИО:", reply_markup=return_to_menu)
        await ChangeUserInfo.next()
    elif m.text == "📬 Адрес":
        await state.update_data(user_choice="address")
        await m.reply("📬️ Введите новый адрес:", reply_markup=return_to_menu)
        await ChangeUserInfo.next()
    elif m.text == "☎️ Номер":
        await state.update_data(user_choice="number")
        await m.reply("☎️ Введите новый номер:", reply_markup=return_to_menu)
        await ChangeUserInfo.next()
    elif m.text == "✖️ Отмена":
        await state.finish()
        await personal_profile(m=m, repo=repo)


async def new_info(m: Message, repo: Repo, state: FSMContext):
    async with state.proxy() as data:
        data['new_info'] = m.text
        change_user = data
    await customer_changed_profile_data(m=m, customer_id=m.chat.id, customer_state_data=change_user, repo=repo)
    await repo.change_user_column(user_id=m.chat.id, column=change_user['user_choice'], data=change_user['new_info'])
    await m.reply(text="👨‍💻 Профиль обновлен!")
    await state.finish()
    await personal_profile(m=m, repo=repo)
