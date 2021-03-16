from aiogram import Bot

from tgbot.config import load_config
from tgbot.services.repository import Repo


async def send_stats(bot: Bot, day: bool, repo: Repo):
    config = load_config("bot.ini")
    if day:
        orders = await repo.get_orders_count(date_range="day")
        if len(orders) > 0:
            day_count = orders[0]['count']

            couriers_stats = {}
            for order in orders:
                if order['courierid'] is not None:
                    if order['courierid'] in couriers_stats:
                        couriers_stats[order['courierid']] += 1
                    else:
                        couriers_stats[order['courierid']] = 1

            if len(couriers_stats) > 0:
                sorted(couriers_stats.items(), key=lambda x: x[1], reverse=True)
                first_courier_from_list = next(iter(couriers_stats))
                courier_of_the_day = await repo.get_courier_by_userid(courier_id=first_courier_from_list)
                courier_of_the_day = f"{courier_of_the_day['name']}\n<b>№{courier_of_the_day['id']}</b>"

                message_to_send = f"""<b>Подведем итоги дня!</b>
    
📦 Всего заказов за день: <b>{day_count}</b>
Курьер дня: <b>{courier_of_the_day}</b>
    
Статистика курьеров:
    """

                i = 1
                for courier in couriers_stats:
                    courier_data = await repo.get_courier_by_userid(courier_id=courier)
                    message_to_send += f"{i}. {courier_data['name']} (№{courier_data['id']}) - {couriers_stats[courier]}\n"
                    i += 1
            else:
                message_to_send = f"""<b>Подведем итоги дня!</b>

📦 Всего заказов за день: <b>{day_count}</b>

<code>Нет статистики по курьерам</code>"""
        else:
            message_to_send = f"""<b>Подведем итоги дня!</b>
            
📦 Всего заказов за день: Заказов не было"""
        await bot.send_message(chat_id=config.tg_bot.orders_group, text=message_to_send)

    else:
        orders = await repo.get_orders_count(date_range="week")
        if len(orders) > 0:
            day_count = orders[0]['count']

            couriers_stats = {}
            for order in orders:
                if order['courierid'] is not None:
                    if order['courierid'] in couriers_stats:
                        couriers_stats[order['courierid']] += 1
                    else:
                        couriers_stats[order['courierid']] = 1

            if len(couriers_stats) > 0:
                sorted(couriers_stats.items(), key=lambda x: x[1], reverse=True)
                first_courier_from_list = next(iter(couriers_stats))
                courier_of_the_week = await repo.get_courier_by_userid(courier_id=first_courier_from_list)
                courier_of_the_week = f"{courier_of_the_week['name']}\n<b>№{courier_of_the_week['id']}</b>"

                message_to_send = f"""<b>Подведем итоги недели!</b>

📦 Всего заказов за неделю: <b>{day_count}</b>
Курьер недели: <b>{courier_of_the_week}</b>

Статистика курьеров:
            """

                i = 1
                for courier in couriers_stats:
                    courier_data = await repo.get_courier_by_userid(courier_id=courier)
                    message_to_send += f"{i}. {courier_data['name']} (№{courier_data['id']}) - {couriers_stats[courier]}\n"
                    i += 1
            else:
                message_to_send = f"""<b>Подведем итоги недели!</b>

📦 Всего заказов за неделю: <b>{day_count}</b>

<i>Нет статистики по курьерам</i>"""
        else:
            message_to_send = f"""<b>Подведем итоги недели!</b>
📦 Всего заказов за неделю: Заказов не было"""
        await bot.send_message(chat_id=config.tg_bot.orders_group, text=message_to_send)
