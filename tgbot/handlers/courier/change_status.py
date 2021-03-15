from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.handlers.courier.personal_profile import personal_profile
from tgbot.keyboards.default.courier.change_status import change_status_kb
from tgbot.services.repository import Repo
from tgbot.states.courier.change_status import ChangeCourierStatus


async def ask_for_status(m: Message):
    await m.reply(text="Выберите статус из списка ниже:",
                  reply_markup=change_status_kb)
    await ChangeCourierStatus.first()


async def set_new_status(m: Message, repo: Repo, state: FSMContext):
    if m.text == "🛵 Свободен":
        await repo.set_courier_status(courier_id=m.chat.id, status="Свободен")
        await state.finish()
        await personal_profile(m=m, repo=repo)
    elif m.text == "🛵❗️ Занят":
        await repo.set_courier_status(courier_id=m.chat.id, status="Занят")
        await state.finish()
        await personal_profile(m=m, repo=repo)
    elif m.text == "📦 На заказе":
        await repo.set_courier_status(courier_id=m.chat.id, status="На заказе")
        await state.finish()
        await personal_profile(m=m, repo=repo)
    elif m.text == "✖️ Отмена":
        await state.finish()
        await personal_profile(m=m, repo=repo)
