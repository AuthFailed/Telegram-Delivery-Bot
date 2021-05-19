from typing import List


class Repo:
    """Db abstraction layer"""

    def __init__(self, conn):
        self.conn = conn

    # promocodes
    async def add_promo(self, promo_name: str, promo_usages: int, promo_code: str = None):
        """
        Регистрация кода
        @param promo_name: Символьное название промокода
        @param promo_usages: Кол-во использований промокода
        @param promo_code: Уникальный набор символов (если не указан - генерируется)
        """
        await self.conn.execute(f"""
INSERT INTO promocodes (promo_name, promo_usages, promo_code) VALUES (\'{promo_name}\', {promo_usages}, \'{promo_code}\'""")

    async def edit_promo(self, promo_code: str, column: str, data: str):
        """
        Редактирование промокода
        @param promo_code: Уникальный набор символов
        @param column: Редактируемый столбец
        @param data: Новые данные
        """
        await self.conn.execute("""
UPDATE promocodes SET {0} = \'{1}\' WHERE promo_code = \'{2}\'""".format(column, data, promo_code))

    async def delete_promo(self, promo_code: str):
        """
        Удаление промокода.
        @param promo_code: Уникальный набор символов
        """
        await self.conn.execute(f"""
DELETE FROM promocodes WHERE promo_code = \'{promo_code}\'""")

    # partners
    async def add_partner(self, userid: int, city: str):
        """
        Добавление партнера
        @param userid: Уникальный идентификатор Telegram
        @param city: Город партнёра
        """
        await self.conn.execute("""
INSERT INTO partners (city, userid) VALUES (\'{0}\', {1})""".format(city, userid))

    async def change_partner_status(self, partner_userid: int, status: bool):
        """
        Изменение статуса партнера
        @param partner_userid: Уникальный идентификатор Telegram
        @param status: Устанавливаемый статус
        @return:
        """
        if status is True:
            await self.conn.execute(
                """UPDATE partners SET working = True WHERE userid = {0}""".format(partner_userid))
        else:
            await self.conn.execute(
                """UPDATE partners SET working = False WHERE userid = {0}""".format(partner_userid))

    async def set_group_id(self, group_type: str, group_id: int, city: str):
        """
        Установка id группы
        @param group_type: Тип группы
        @param group_id: Уникальный идентификатор Telegram
        @param city: Город партнёра
        @return:
        """
        await self.conn.execute("""
UPDATE partners SET {0} = {1} WHERE city = \'{2}\'""".format(group_type, group_id, city)
                                )

    async def is_partner_exists(self, city: str = None, userid=None):
        """
        Существует ли партнёр
        @param city: Город партнёра
        @param userid: Уникальный идентификатор Telegram
        @return:
        """
        if city is None:
            result = await self.conn.fetchval(
                "SELECT EXISTS("
                "SELECT 1 "
                "FROM partners "
                "WHERE userid='{0}')".format(userid)
            )
        else:
            result = await self.conn.fetchval(
                "SELECT EXISTS("
                "SELECT 1 "
                "FROM partners "
                "WHERE city='{0}')".format(city)
            )
        return result

    async def get_partner(self, city: str = None, userid: int = None):
        """
        Получить данные партнёра
        @param city: Город партнёра
        @param userid: Уникальный идентификатор Telegram
        @return:
        """
        if city is None:
            result = await self.conn.fetchrow("""
SELECT * FROM partners WHERE userid = \'{0}\'""".format(userid))
        else:
            result = await self.conn.fetchrow("""
SELECT * FROM partners WHERE city = \'{0}\'""".format(city))
        return result

    async def get_partners(self, with_main: bool = False):
        """
        Получить всех партнеров
        @param with_main: С администратором?
        @return: 
        """
        execute_request = "SELECT * FROM partners"
        if with_main is False:
            execute_request += " WHERE main = False"
        execute_request += " ORDER BY city"
        rows = await self.conn.fetch(execute_request)
        return rows

    async def get_available_cities(self):
        """
        Получить доступные (включенные) города
        @return:
        """
        result = await self.conn.fetch(
            """SELECT * FROM partners WHERE working = True ORDER BY city"""
        )
        return result

    async def delete_partner(self, city: str = None, userid: int = None):
        """
        Удалить партнёра
        @param city: Город партнёра
        @param userid: Уникальный идентификатор Telegram
        @return:
        """
        if city is None:
            await self.conn.execute("""
DELETE FROM partners WHERE userid = {0}""".format(userid))
        else:
            await self.conn.execute("""
            DELETE FROM partners WHERE city = \'{0}\'""".format(city))

    # managers
    async def add_manager(self, userid: int, name: str, city: str, number: str):
        """
        Добавить менеджера
        @param userid: Уникальный идентификатор Telegram
        @param name: Фио менеджера
        @param city: Город менеджера
        @param number: Номер менеджера
        @return:
        """
        await self.conn.execute("""
INSERT INTO managers (userid, city, name, number)
VALUES ({0}, \'{1}\', \'{2}\', \'{3}\')""".format(userid, city, name, number))

    async def get_manager(self, userid):
        """
        Получить данные менеджера
        @param userid:
        @return:
        """
        result = await self.conn.fetchrow("""
SELECT * FROM managers WHERE userid={0}""".format(userid))
        return result

    async def is_manager_exists(self, userid):
        """
        Проверка существует ли менеджер
        @param userid: Уникальный идентификатор Telegram
        @return:
        """
        result = await self.conn.fetchval("""
SELECT EXISTS(
SELECT 1
FROM managers
WHERE userid={0})
""".format(userid))
        return result

    async def delete_manager(self, userid):
        """
        Удалить менеджера
        @param userid: Уникальный идентификатор Telegram
        @return:
        """
        await self.conn.execute("""
DELETE FROM managers WHERE userid = {0}""".format(userid))

    async def get_managers_list(self, city: str = None):
        """
        Получить список менеджеров
        @param city: Город менеджеров
        @return:
        """
        if city is None:
            result = await self.conn.fetch("""
SELECT * FROM managers ORDER BY name""")
        else:
            result = await self.conn.fetch("""
SELECT * FROM managers WHERE city=\'{0}\' ORDER BY name""".format(city))
        return result

    # users
    async def add_customer(self, userid: int, user_type: str, name: str, city: str, address: str, number: str,
                           referral=None) -> None:
        """
        Добавить заказчика
        @param referral: Уникальный идентификатор Telegram пригласившего
        @param userid: Уникальный идентификатор Telegram
        @param user_type: Тип заказчика (Компания/Частное лицо)
        @param name: Фио заказчика
        @param city: Город заказчика
        @param address: Адрес заказчика
        @param number: Номер заказчика
        @return:
        """
        if referral:
            result = await self.conn.fetchval(
                "INSERT INTO customers (userid, referral, usertype, name, city, address, number) "
                "VALUES ({0}, {1}, \'{2}\', \'{3}\', \'{4}\', \'{5}\', \'{6}\') "
                "ON CONFLICT DO NOTHING "
                "RETURNING id".format(userid,
                                      referral,
                                      user_type,
                                      name,
                                      city,
                                      address,
                                      number),
            )
        else:
            result = await self.conn.fetchval(
                "INSERT INTO customers (userid, usertype, name, city, address, number) "
                "VALUES ({0}, \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\') "
                "ON CONFLICT DO NOTHING "
                "RETURNING id".format(userid,
                                      user_type,
                                      name,
                                      city,
                                      address,
                                      number),
            )
        return result

    async def get_customer(self, userid: int = None, serial_id: int = None):
        """
        Получить данные заказчика
        @param userid: Уникальный идентификатор Telegram
        @param serial_id: Инкрементный id заказчика
        @return:
        """
        if serial_id is None:
            result = await self.conn.fetchrow(
                "SELECT * "
                "FROM customers "
                "WHERE userid = {0}".format(userid)
            )
        else:
            result = await self.conn.fetchrow(
                "SELECT * "
                "FROM customers "
                "WHERE id = {0}".format(serial_id)
            )
        return result

    async def check_referrals(self, userid: int):
        query = "SELECT chat_id FROM users WHERE referral=" \
                "(SELECT id FROM users WHERE chat_id={0})".format(userid)
        result = await self.conn.fetch(query)
        return result

    async def edit_customer_column(self, userid: int, column: str, data: str):
        """
        Редактирование данных заказчика
        @param userid: Уникальный идентификатор Telegram
        @param column: Редактируемый столбец
        @param data: Новые данные
        @return:
        """
        await self.conn.execute(
            "UPDATE customers "
            "SET {0} = \'{1}\' "
            "WHERE userid = {2}".format(column, data, userid)
        )

    async def get_customer_orders(self, userid: int):
        """
        Получить список заказов пользователя
        @param userid: Уникальный идентификатор Telegram
        @return:
        """
        rows = await self.conn.fetch(
            "SELECT * "
            "FROM orders "
            "WHERE customerid = {0} "
            "ORDER BY id DESC".format(userid)
        )
        return [dict(row) for row in rows]

    async def is_customer_exists(self, user_id: int):
        """
        Проверка существует ли заказчик
        @param user_id:
        @return:
        """
        result = await self.conn.fetchval(
            "SELECT EXISTS("
            "SELECT 1 "
            "FROM customers "
            "WHERE userid={0})".format(user_id)
        )
        return result

    async def get_customers_list(self, city_name: str = None) -> List[int]:
        """
        Получить список заказчиков
        @param city_name: Город заказчиков
        @return:
        """
        if city_name is None:
            result = await self.conn.fetch(
                "select * "
                "from customers ORDER BY name"
            )
        else:
            result = await self.conn.fetch(
                "select * "
                "from customers"
                "where city=\'{0}\' ORDER BY name".format(city_name)
            )
        return result

    async def delete_customer(self, userid: int):
        """
        Удалить заказчика
        @param userid: Уникальный идентификатор Telegram
        @return:
        """
        await self.conn.execute(
            "DELETE FROM customers "
            "WHERE userid = {0}".format(userid)
        )

    # couriers
    async def add_courier(self, userid: int, name: str, city: str, number: str, passport_main_id: str,
                          passport_registration_id: str, driver_license_front_id: str, driver_license_back_id: str,
                          applied: bool = False):
        """
        Добавить курьера
        @param userid: Уникальный идентификатор Telegram
        @param name: Фио курьера
        @param city: Город курьера
        @param number: Номер курьера
        @param passport_main_id: Уникальный идентификатор фото главной страницы
        @param passport_registration_id: Уникальный идентификатор фото регистрации
        @param driver_license_front_id: Уникальный идентификатор фото водител. удостоверения
        @param driver_license_back_id: Уникальный идентификатор фото водител. удостоверения обратной стороны
        @param applied: Подтвердить?
        @return:
        """
        courier_data = await self.conn.fetch(
            "INSERT INTO couriers"
            "(userid, city, name, number, passportmain, passportregistration, driverlicensefront, driverlicenseback, applied) "
            "VALUES ({0}, \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\', \'{6}\', \'{7}\', {8}) "
            "RETURNING id, name, city, number, passportmain, passportregistration, driverlicensefront, "
            "driverlicenseback, status".format(
                userid,
                city,
                name,
                number,
                passport_main_id,
                passport_registration_id,
                driver_license_front_id,
                driver_license_back_id,
                applied)
        )
        return courier_data

    async def is_courier_exists(self, userid):
        """
        Существует ли курьер
        @param userid: Уникальный идентификатор Telegram
        @return:
        """
        result = await self.conn.fetchval("""
    SELECT EXISTS(
    SELECT 1
    FROM managers
    WHERE userid={0})
    """.format(userid))
        return result

    async def get_courier(self, userid: int = None, serial_id: int = None):
        """
        Получить данные курьера
        @param userid: Уникальный идентификатор Telegram
        @param serial_id: Инкрементный id курьера
        @return:
        """
        if serial_id is None:
            result = await self.conn.fetchrow(
                "SELECT * "
                "FROM couriers "
                "WHERE userid = {0}".format(userid)
            )
        else:
            result = await self.conn.fetchrow(
                "SELECT * "
                "FROM couriers "
                "WHERE id = {0}".format(serial_id)
            )
        return result

    async def get_couriers_orders(self, userid: int):
        """
        Получить заказы курьера
        @param userid: Уникальный идентификатор Telegram курьера
        @return:
        """
        rows = await self.conn.fetch(
            "SELECT * "
            "FROM orders "
            "WHERE courierid = {0} ORDER BY id DESC".format(userid)
        )
        return [dict(row) for row in rows]

    async def get_couriers_list(self, city: str = None):
        """
        Получить список курьеров
        @param city: Город курьеров
        @return:
        """
        if city is None:
            result = await self.conn.fetch("""
    SELECT * FROM couriers ORDER BY name""")
        else:
            result = await self.conn.fetch("""
    SELECT * FROM couriers WHERE city=\'{0}\' ORDER BY name""".format(city))
        return result

    async def get_available_couriers_list(self, city: str) -> list[any]:
        """
        Получить список доступных курьеров
        @param city: Город курьеров
        @return:
        """
        rows = await self.conn.fetch(
            "SELECT * from couriers WHERE applied = True and city = \'{0}\' ORDER BY name".format(city)
        )
        return [dict(row) for row in rows]

    async def set_courier_apply_status(self, userid: int, applied: bool):
        """
        Установить статус активации курьера
        @param userid: Уникальный идентификатор Telegram
        @param applied: Устанавливаемый статус
        @return:
        """
        await self.conn.execute(
            "UPDATE couriers SET applied = {0} WHERE userid = {1}".format(applied, userid)
        )

    async def set_courier_status(self, userid: int, status: str):
        """
        Установить статус курьера
        @param userid: Уникальный идентификатор Telegram
        @param status: Устанавливаемый статус
        @return:
        """
        await self.conn.execute(
            "UPDATE couriers SET status = \'{0}\' WHERE userid = {1}".format(status, userid)
        )

    async def delete_courier(self, userid: int):
        """
        Удалить курьера
        @param userid: Уникальный идентификатор Telegram
        @return:
        """
        await self.conn.execute(
            "DELETE FROM couriers WHERE userid = {0}".format(userid)
        )

    # orders
    async def add_order(self,
                        city: str,
                        customer_userid: int,
                        customer_type: str,
                        customer_name: str,
                        customer_address: str,
                        customer_number: str,
                        order_name: str,
                        order_address: str,
                        order_number: str,
                        order_time: str,
                        other_details: str):
        """
        Добавить заказ
        @param city: Город заказа
        @param customer_userid: Уникальный идентификатор Telegram заказчика
        @param customer_type: Тип заказчика (Компания/Частное лицо
        @param customer_name: Фио заказчика
        @param customer_address: Адрес заказчика
        @param customer_number: Номер заказчика
        @param order_name: Фио получателя
        @param order_address: Адрес получателя
        @param order_number: Номер получателя
        @param order_time: Дата и время доставки
        @param other_details: Другие детали заказа
        @return:
        """
        order_id = await self.conn.fetchval(
            "INSERT INTO orders "
            "(city, customerid, customertype, customername, customeraddress, customernumber, ordername, orderaddress, "
            "ordernumber, ordertime, otherdetails) "
            "VALUES (\'{0}\', {1}, \'{2}\', \'{3}\', \'{4}\', \'{5}\', \'{6}\', \'{7}\', \'{8}\', \'{9}\', "
            "\'{10}\') "
            "RETURNING "
            "id".format(city, customer_userid, customer_type, customer_name, customer_address, customer_number,
                        order_name, order_address, order_number, order_time, other_details)
        )
        return order_id

    async def get_order(self, order_id: int):
        """
        Получить данные заказа
        @param order_id: Уникальный идентификатор Telegram
        @return:
        """
        result = await self.conn.fetchrow(
            "SELECT * FROM orders WHERE id = {0}".format(order_id)
        )
        return result

    async def change_order_status(self, order_id: int, order_status: str):
        """
        Сменить статус заказа
        @param order_id: Инкрементный идентификатор заказа
        @param order_status: Устанавливаемый статус
        @return:
        """
        await self.conn.execute(
            "UPDATE orders SET status = \'{0}\' WHERE id = {1}".format(order_status, order_id)
        )

    async def change_order_courier(self, order_id: int, courier_userid: int):
        """
        Сменить курьера у заказа
        @param order_id: Инкрементный идентификатор заказа
        @param courier_userid: Уникальный идентификатор Telegram курьера
        @return:
        """
        await self.conn.execute(
            "UPDATE orders SET courierid = {0} WHERE id = {1}".format(courier_userid, order_id)
        )

    async def get_orders_list(self, city: str = None):
        """
        Получить список заказов
        @param city: Город заказов
        @return:
        """
        if city is None:
            result = await self.conn.fetch("""
    SELECT * FROM orders by id""")
        else:
            result = await self.conn.fetch("""
    SELECT * FROM orders WHERE city=\'{0}\' ORDER BY id""".format(city))
        return result

    # @TODO доделать статистику
    async def get_orders_count(self, city: str, date_range: str, courier_userid: int = None):
        """
        Получить кол-во заказов
        @param city: Город заказов
        @param date_range: Период
        @param courier_userid: Уникальный идентификатор Telegram курьера
        @return:
        """
        if courier_userid is None:
            result = await self.conn.fetch(
                """SELECT *, date_trunc('{0}', orders.registerdate),
                 count(1) FROM orders WHERE city={1} GROUP BY 1""".format(date_range, city)
            )
        else:
            result = await self.conn.fetch(
                """SELECT *, date_trunc('{0}', orders.registerdate),
                 count(1) FROM orders WHERE city={1} and courierid={2} GROUP BY 1""".format(
                    date_range, city, courier_userid)
            )
        return result
