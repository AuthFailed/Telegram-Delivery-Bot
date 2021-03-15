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
                courier_of_the_day = f"{courier_of_the_day['name']}\n№{courier_of_the_day['id']}"

                message_to_send = f"""*Подведем итоги дня!*
    
📦 Всего заказов за день: *{day_count}*
Курьер дня: *{courier_of_the_day}*
    
Статистика курьеров:
    """

                i = 1
                for courier in couriers_stats:
                    courier_data = await repo.get_courier_by_userid(courier_id=courier)
                    message_to_send += f"{i}. {courier_data['name']} (№{courier_data['id']}) - {couriers_stats[courier]}\n"
                    i += 1
            else:
                message_to_send = f"""*Подведем итоги дня!*

📦 Всего заказов за день: *{day_count}*

_Нет статистики по курьерам_"""
        else:
            message_to_send = f"""*Подведем итоги дня!*
            
📦 Всего заказов за день: Заказов не было"""
        await bot.send_message(chat_id=config.tg_bot.orders_group, text=message_to_send, parse_mode='Markdown')

    # courier_of_the_day = "Нет информации"
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
                courier_of_the_week = f"{courier_of_the_week['name']}\n№{courier_of_the_week['id']}"

                message_to_send = f"""*Подведем итоги недели!*

📦 Всего заказов за неделю: *{day_count}*
Курьер недели: *{courier_of_the_week}*

Статистика курьеров:
            """

                i = 1
                for courier in couriers_stats:
                    courier_data = await repo.get_courier_by_userid(courier_id=courier)
                    message_to_send += f"{i}. {courier_data['name']} (№{courier_data['id']}) - {couriers_stats[courier]}\n "
                    i += 1
            else:
                message_to_send = f"""*Подведем итоги недели!*

📦 Всего заказов за неделю: *{day_count}*

_Нет статистики по курьерам_"""
        else:
            message_to_send = f"""*Подведем итоги недели!*
📦 Всего заказов за неделю: Заказов не было"""
        await bot.send_message(chat_id=config.tg_bot.orders_group, text=message_to_send, parse_mode='Markdown')
