from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from tgbot.handlers.customer.personal_profile import personal_profile
from tgbot.keyboards.default.user.delete_profile import delete_profile_kb
from tgbot.services.event_handlers import customer_delete_profile
from tgbot.services.repository import Repo
from tgbot.states.user.delete_profile import DeleteProfile


async def delete_profile(m: Message):
    await m.reply("‼️ Вы уверены, что хотите удалить свой профиль?\n"
                  "Оформленные вами заказы станут доступны при повторной регистрации.", reply_markup=delete_profile_kb)
    await DeleteProfile.first()


async def delete_profile_yes(m: Message, state: FSMContext, repo: Repo):
    customer_data = await repo.get_customer(user_id=m.chat.id)
    await customer_delete_profile(m=m, customer_data=customer_data)
    await repo.delete_customer(user_id=m.chat.id)
    await m.reply(text="🔨 <b>Ваш аккаунт был удален!</b>\n"
                       "Для повторной регистрации используйте команду /start",
                  reply_markup=ReplyKeyboardRemove())
    await state.finish()


async def delete_profile_no(m: Message, state: FSMContext, repo: Repo):
    await state.finish()

    await personal_profile(m=m, repo=repo)
