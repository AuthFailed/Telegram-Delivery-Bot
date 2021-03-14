from typing import List


class Repo:
    """Db abstraction layer"""

    def __init__(self, conn):
        self.conn = conn

    # users
    async def add_user(self, user_id: int, user_type: str, name: str, address: str, number: str) -> None:
        """Store user in DB, ignore duplicates"""
        result = await self.conn.fetchval(
            "INSERT INTO customers (UserId, UserType, Name, Address, Number)" \
            " VALUES ({0}, \'{1}\', \'{2}\', \'{3}\', \'{4}\') ON CONFLICT DO NOTHING RETURNING id".format(user_id,
                                                                                                           user_type,
                                                                                                           name,
                                                                                                           address,
                                                                                                           number),
        )
        return result

    async def get_user(self, user_id: int):
        """Get full user data from DB"""
        result = await self.conn.fetchrow(
            "SELECT * FROM customers WHERE UserId = $1",
            user_id
        )
        return result

    async def change_user_column(self, user_id: int, column: str, data: str):
        """Change user data in certain column"""
        await self.conn.execute(
            "UPDATE customers SET {0} = \'{1}\' WHERE userid = {2}".format(column, data, user_id)
        )

    async def get_user_orders(self, user_id: int):
        rows = await self.conn.fetch(
            "SELECT * FROM orders WHERE customerid = $1 ORDER BY orderid DESC",
            user_id
        )
        return [dict(row) for row in rows]

    async def is_user_exists(self, user_id: int):
        result = await self.conn.fetchval(
            "SELECT EXISTS(SELECT 1 FROM customers WHERE UserId=$1)",
            user_id
        )
        return result

    async def list_users(self) -> List[int]:
        """List all bot users"""
        return [
            row[0]
            async for row in self.conn.execute(
                "select * from customers",
            )
        ]

    async def delete_user(self, user_id: int):
        """Remove user from DB"""
        await self.conn.execute(
            "DELETE FROM customers WHERE userid = $1",
            user_id
        )

    # couriers
    async def add_courier(self, user_id: int, name: str, number: str, passport_main_id: str,
                          passport_registration_id: str, driver_license_front_id: str, driver_license_back_id: str):
        """Add courier to DB"""
        courier_data = await self.conn.fetch(
            "INSERT INTO couriers(UserId, Name, Number, PassportMain, PassportRegistration, DriverLicenseFront, DriverLicenseBack) "
            "VALUES ({0}, \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\', \'{6}\') "
            "RETURNING id, name, number, PassportMain, PassportRegistration, DriverLicenseFront, DriverLicenseBack".format(
                user_id,
                name,
                number,
                passport_main_id,
                passport_registration_id,
                driver_license_front_id,
                driver_license_back_id)
        )
        return courier_data

    async def get_courier_by_userid(self, courier_id: int):
        """Get full user data from DB"""
        result = await self.conn.fetchrow(
            "SELECT * FROM couriers WHERE userid = {0}".format(courier_id)
        )
        return result

    async def get_courier_by_id(self, courier_id: int):
        """Get full user data from DB"""
        result = await self.conn.fetchrow(
            "SELECT * FROM couriers WHERE id = {0}".format(courier_id)
        )
        return result

    async def get_couriers_orders(self, courier_id: int):
        """Get all orders completed by courier"""
        rows = await self.conn.fetch(
            "SELECT * FROM orders WHERE courierid = $1",
            courier_id
        )
        return [dict(row) for row in rows]

    async def get_couriers_list(self):
        """Get couriers list"""
        rows = await self.conn.fetch(
            "SELECT userid FROM couriers"
        )
        return [dict(row) for row in rows]

    async def get_available_couriers_list(self):
        """Get available couriers from DB"""
        rows = await self.conn.fetch(
            "SELECT * from couriers WHERE status = \'Свободен\'"
        )
        return [dict(row) for row in rows]

    async def change_courier_apply_status(self, courier_id: int, applied: bool):
        await self.conn.execute(
            "UPDATE couriers SET applied = {0} WHERE userid = {1}".format(applied, courier_id)
        )

    async def change_courier_status(self, courier_id: int, status: str):
        """Change courier status"""
        await self.conn.execute(
            "UPDATE couriers SET status = \'{0}\' WHERE userid = {1}".format(status, courier_id)
        )

    # orders
    async def add_order(self,
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
            "(CustomerId, CustomerType, CustomerName, CustomerAddress, CustomerNumber, OrderName, OrderAddress, "
            "OrderNumber, OrderTime, OtherDetails) "
            "VALUES ({0}, \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\', \'{6}\', \'{7}\', \'{8}\', \'{9}\') RETURNING "
            "orderid".format(customer_id, customer_type, customer_name, customer_address, customer_number, order_name,
                             order_address, order_number, order_time, other_details)
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
            "UPDATE orders SET Courierid = {0} WHERE orderid = {1}".format(courier_id, order_id)
        )

    # stats
    async def get_orders_count(self, date_range: str):
        """Get orders count by date range"""
        result = await self.conn.fetchval(
            """select date_trunc('$1', orders.CurrentTime), count(1) from orders group by 1;""",
            date_range
        )
        return result
