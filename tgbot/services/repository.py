from typing import List


class Repo:
    """Db abstraction layer"""

    def __init__(self, conn):
        self.conn = conn

    # partners
    async def add_partner(self, partner_id: int, city: str):
        await self.conn.execute("""
INSERT INTO partners (city, adminid) VALUES (\'{0}\', {1})""".format(city, partner_id))

    async def change_partner_status(self, partner_id: int, status: bool):
        if status is True:
            await self.conn.execute("""UPDATE partners SET isworking = True WHERE adminid = {0}""".format(partner_id))
        else:
            await self.conn.execute("""UPDATE partners SET isworking = False WHERE adminid = {0}""".format(partner_id))

    async def set_group_id(self, group: str, group_id: int, city: str):
        await self.conn.execute("""
UPDATE partners SET {0} = {1} WHERE city = \'{2}\'""".format(group, group_id, city)
                                )

    async def is_partner_exists(self, city: str = None, partner_id=None):
        if city is None:
            result = await self.conn.fetchval(
                "SELECT EXISTS("
                "SELECT 1 "
                "FROM partners "
                "WHERE adminid=$1)",
                partner_id
            )
        else:
            result = await self.conn.fetchval(
                "SELECT EXISTS("
                "SELECT 1 "
                "FROM partners "
                "WHERE city=$1)",
                city
            )
        return result

    async def get_partner(self, city: str = None, admin_id: str = None):
        if city is None:
            result = await self.conn.fetchrow("""
SELECT * FROM partners WHERE adminid = \'{0}\'""".format(admin_id))
        else:
            result = await self.conn.fetchrow("""
SELECT * FROM partners WHERE city = \'{0}\'""".format(city))
        return result

    async def get_partners(self, with_main: bool = False):
        """Get all available cities"""
        execute_request = "SELECT * FROM partners"
        if with_main is False:
            execute_request += " WHERE ismain = False"
        rows = await self.conn.fetch(execute_request)
        return rows

    async def get_available_cities(self):
        result = await self.conn.fetch(
            """SELECT * FROM partners WHERE isworking = True"""
        )
        return result

    async def delete_partner(self, city: str = None, admin_id: str = None):
        if city is None:
            await self.conn.execute("""
DELETE FROM partners WHERE adminid = {0}""".format(admin_id))
        else:
            await self.conn.execute("""
            DELETE FROM partners WHERE city = \'{0}\'""".format(city))

    # managers
    async def add_manager(self, user_id: int, name: str, city: str, number: str):
        result = await self.conn.fetchval("""
INSERT INTO managers (userid, name, city, number)
VALUES ({0}, {1}, {2}, {3})
ON CONFLICT DO NOTHING
RETURNING id
""".format(user_id, name, city, number))
        return result

    async def get_manager(self, manager_id: int):
        result = await self.conn.fetchrow("""
SELECT * FROM managers WHERE userid={0}""".format(manager_id))
        return result

    async def delete_manager(self, user_id):
        await self.conn.execute("""
DELETE FROM managers WHERE userid = {0}""".format(user_id))

    async def get_managers_list(self, city: str = None):
        if city is None:
            result = await self.conn.fetch("""
SELECT * FROM managers""")
        else:
            result = await self.conn.fetch("""
SELECT * FROM managers WHERE city=\'{0}\'""".format(city))
        return result

    # users
    async def add_user(self, user_id: int, user_type: str, name: str, city: str, address: str, number: str) -> None:
        """Store user in DB, ignore duplicates"""
        result = await self.conn.fetchval(
            "INSERT INTO customers (userid, usertype, name, city, address, number) "
            "VALUES ({0}, \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\') "
            "ON CONFLICT DO NOTHING "
            "RETURNING id".format(user_id,
                                  user_type,
                                  name,
                                  city,
                                  address,
                                  number),
        )
        return result

    async def get_customer(self, user_id: int = None, id: int = None):
        """Get full user data from DB"""
        if id is None:
            result = await self.conn.fetchrow(
                "SELECT * "
                "FROM customers "
                "WHERE userid = $1",
                user_id
            )
        else:
            result = await self.conn.fetchrow(
                "SELECT * "
                "FROM customers "
                "WHERE id = $1",
                id
            )
        return result

    async def change_user_column(self, user_id: int, column: str, data: str):
        """Change user data in certain column"""
        await self.conn.execute(
            "UPDATE customers "
            "SET {0} = \'{1}\' "
            "WHERE userid = {2}".format(column, data, user_id)
        )

    async def get_customer_orders(self, user_id: int):
        rows = await self.conn.fetch(
            "SELECT * "
            "FROM orders "
            "WHERE customerid = $1 "
            "ORDER BY orderid DESC",
            user_id
        )
        return [dict(row) for row in rows]

    async def is_user_exists(self, user_id: int):
        result = await self.conn.fetchval(
            "SELECT EXISTS("
            "SELECT 1 "
            "FROM customers "
            "WHERE UserId=$1)",
            user_id
        )
        return result

    async def get_customers_list(self, city_name: str = None) -> List[int]:
        """List all bot users"""
        if city_name is None:
            result = await self.conn.fetch(
                "select * "
                "from customers"
            )
        else:
            result = await self.conn.fetch(
                "select * "
                "from customers"
                "where city=\'{0}\'".format(city_name)
            )
        return result

    async def delete_customer(self, user_id: int):
        """Remove user from DB"""
        await self.conn.execute(
            "DELETE FROM customers "
            "WHERE userid = $1",
            user_id
        )

    # couriers
    async def add_courier(self, user_id: int, name: str, city: str, number: str, passport_main_id: str,
                          passport_registration_id: str, driver_license_front_id: str, driver_license_back_id: str):
        """Add courier to DB"""
        courier_data = await self.conn.fetch(
            "INSERT INTO couriers"
            "(userid, name, city, number, passportmain, passportregistration, driverlicensefront, driverlicenseback) "
            "VALUES ({0}, \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\', \'{6}\', \'{7}\') "
            "RETURNING id, name, city, number, passportmain, passportregistration, driverlicensefront, "
            "driverlicenseback".format(
                user_id,
                name,
                city,
                number,
                passport_main_id,
                passport_registration_id,
                driver_license_front_id,
                driver_license_back_id)
        )
        return courier_data

    async def get_courier(self, courier_id: int = None, id: int = None):
        """Get full user data from DB"""
        if id is None:
            result = await self.conn.fetchrow(
                "SELECT * "
                "FROM couriers "
                "WHERE userid = {0}".format(courier_id)
            )
        else:
            result = await self.conn.fetchrow(
                "SELECT * "
                "FROM couriers "
                "WHERE id = {0}".format(id)
            )
        return result

    async def get_couriers_orders(self, courier_id: int):
        """Get all orders completed by courier"""
        rows = await self.conn.fetch(
            "SELECT * "
            "FROM orders "
            "WHERE courierid = {0}".format(courier_id)
        )
        return [dict(row) for row in rows]

    async def get_couriers_list(self) -> list[any]:
        """Get couriers list"""
        rows = await self.conn.fetch(
            "SELECT userid FROM couriers"
        )
        return [dict(row) for row in rows]

    async def get_available_couriers_list(self, city: str) -> list[any]:
        """Get available couriers from DB"""
        rows = await self.conn.fetch(
            "SELECT * from couriers WHERE applied = True and city = \'{0}\'".format(city)
        )
        return [dict(row) for row in rows]

    async def set_courier_apply_status(self, courier_id: int, applied: bool):
        await self.conn.execute(
            "UPDATE couriers SET applied = {0} WHERE userid = {1}".format(applied, courier_id)
        )

    async def set_courier_status(self, courier_id: int, status: str):
        """Change courier status"""
        await self.conn.execute(
            "UPDATE couriers SET status = \'{0}\' WHERE userid = {1}".format(status, courier_id)
        )

    async def delete_courier(self, courier_id: int):
        """Delete courier from DB"""
        await self.conn.execute(
            "DELETE FROM couriers WHERE userid = {0}".format(courier_id)
        )

    # orders
    async def add_order(self,
                        city: str,
                        customer_id: int,
                        customer_type: str,
                        customer_name: str,
                        customer_address: str,
                        customer_number: str,
                        order_name: str,
                        order_address: str,
                        order_number: str,
                        order_time: str,
                        other_details: str):
        """Store order in db"""
        order_id = await self.conn.fetchval(
            "INSERT INTO orders "
            "(city, customerid, customertype, customername, customeraddress, customernumber, ordername, orderaddress, "
            "ordernumber, ordertime, otherdetails) "
            "VALUES (\'{0}\', {1}, \'{2}\', \'{3}\', \'{4}\', \'{5}\', \'{6}\', \'{7}\', \'{8}\', \'{9}\', \'{10}\') "
            "RETURNING "
            "orderid".format(city, customer_id, customer_type, customer_name, customer_address, customer_number,
                             order_name, order_address, order_number, order_time, other_details)
        )
        return order_id

    async def get_order(self, order_id: int):
        """Get order info by order_id"""
        result = await self.conn.fetchrow(
            "SELECT * FROM orders WHERE orderid = {0}".format(order_id)
        )
        return result

    async def change_order_status(self, order_id: int, order_status: str):
        """Change order status by order_id"""
        await self.conn.execute(
            "UPDATE orders SET status = \'{0}\' WHERE orderid = {1}".format(order_status, order_id)
        )

    async def change_order_courier(self, order_id: int, courier_id: int):
        await self.conn.execute(
            "UPDATE orders SET courierid = {0} WHERE orderid = {1}".format(courier_id, order_id)
        )

    # stats
    async def get_orders_count(self, date_range: str, courier_id: int = None):
        """Get orders count by date range"""
        if courier_id is None:
            result = await self.conn.fetch(
                """SELECT *, date_trunc('{0}', orders.currenttime), count(1) FROM orders GROUP BY 1""".format(
                    date_range)
            )
        else:
            result = await self.conn.fetch(
                "7".format(
                    date_range, courier_id)
            )
        return result
