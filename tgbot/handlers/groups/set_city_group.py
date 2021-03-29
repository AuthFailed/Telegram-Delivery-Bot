from aiogram.types import Message

from tgbot.services.repository import Repo


async def set_orders_group(m: Message, repo: Repo):
    city_data = await repo.get_partner(admin_id=m.from_user.id)
    await repo.set_group_id(group='ordersgroupid', group_id=m.chat.id, city=city_data['city'])
    await m.answer(text=f"✅ Группа <b>{m.chat.title}</b> установлена как группа <b>приходящих заказов</b> у города <b>{city_data['city'].title()}</b>.")


async def set_couriers_group(m: Message, repo: Repo):
    city_data = await repo.get_partner(admin_id=m.from_user.id)
    await repo.set_group_id(group='couriersgroupid', group_id=m.chat.id, city=city_data['city'])
    await m.answer(text=f"✅ Группа <b>{m.chat.title}</b> установлена как группа <b>регистраций курьеров</b> у города <b>{city_data['city'].title()}</b>.")


async def set_events_group(m: Message, repo: Repo):
    city_data = await repo.get_partner(admin_id=m.from_user.id)
    await repo.set_group_id(group='eventsgroupid', group_id=m.chat.id, city=city_data['city'])
    await m.answer(text=f"✅ Группа <b>{m.chat.title}</b> установлена как <b>группа событий</b> у города <b>{city_data['city'].title()}</b>.")

