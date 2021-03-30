from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.default.admin.main_menu import main_menu
from tgbot.services import Repo


async def start(m: Message, repo: Repo, state: FSMContext = None):
    if state is not None:
        await state.finish()

    admin_data = await repo.get_partner(admin_id=m.chat.id)
    if admin_data['ordersgroupid'] is None:
        await m.answer(text="⚠️ У Вас не установлена группа для заказов."
                            "\nИспользуйте команду /setting_groups для помощи.")
    if admin_data['couriersgroupid'] is None:
        await m.answer(text="⚠️ У Вас не установлена группа для заявок курьеров."
                            "\nИспользуйте команду /setting_groups для настройки.")
    if admin_data['eventsgroupid'] is None:
        await m.answer(text="⚠️ У Вас не установлена группа для событий."
                            "\nИспользуйте команду /setting_groups для настройки.")
    await m.answer(text="Главное меню",
                   reply_markup=main_menu)
