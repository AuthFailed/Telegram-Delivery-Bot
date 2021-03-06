from aiogram.types import Message


async def setting_groups(m: Message):
    await m.answer(text="""⚠️ Перед работой с ботом Вам необходимо настроить <b>группы</b>.

Первым дело создайте 3 группы, которые будут отвечать за следующее:
1. 🛍 <b>Приходящие заказы</b>
<i>Поступление новых заказов, изменение их статусов, выбор курьеров.</i>
2. 🚚 <b>Заявки от новых курьеров</b>
<i>Поступление и обработку заявок на регистрацию курьеров. Пропускной пункт.</i>
3. 🎃 <b>События</b>
<i>Отвечает за все события, происходящие в боте: Создание заказа, новая регистрация, удаление профиля, изменение личных данных и т.п.</i>

🤖 После создания этих групп, Вам понадобится <b>добавить меня (@Dostavka30rus_bot) в каждую из них</b> и <b>выдать права администратора</b>.

📝 Затем, чтобы я запомнил, какая группа для чего нужна, <b>используй в нужной группе одну из следующих команд</b>:
● /set_orders_group
<i>Установка группы приходящих заявок</i>
● /set_couriers_group
<i>Установка группы заявок новых курьеров</i>
● /set_events_group
<i>Установка группы событий</i>""")
