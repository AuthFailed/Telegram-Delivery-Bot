from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from tgbot.handlers.customer.personal_profile import personal_profile
from tgbot.keyboards.default.courier.delete_profile import delete_profile_kb
from tgbot.services.event_handlers import courier_delete_profile
from tgbot.services.repository import Repo
from tgbot.states.courier.delete_profile import DeleteAccount


async def delete_profile(m: Message):
    await m.reply("‼️ Вы уверены, что хотите удалить свой профиль?\n"
                  "Выполненные вами заказы станут доступны при повторной регистрации.", reply_markup=delete_profile_kb)
    await DeleteAccount.first()


async def delete_profile_yes(m: Message, state: FSMContext, repo: Repo):
    courier_data = await repo.get_courier_by_userid(courier_id=m.chat.id)
    await courier_delete_profile(m=m, courier_data=courier_data)
    await repo.delete_courier(courier_id=m.chat.id)
    await m.reply(text="🔨 *Ваш аккаунт был удален\!*\n"
                       "Для повторной регистрации используйте команду /start",
                  reply_markup=ReplyKeyboardRemove(),
                  parse_mode="MarkdownV2")
    await state.finish()


async def delete_profile_no(m: Message, state: FSMContext, repo: Repo):
    await state.finish()

    await personal_profile(m=m, repo=repo)
