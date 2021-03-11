from typing import List


class Repo:
    """Db abstraction layer"""

    def __init__(self, conn):
        self.conn = conn

    # users
    async def add_user(self, user_id: int, user_type: str, name: str, address: str, number: str) -> None:
        """Store user in DB, ignore duplicates"""
        await self.conn.execute(
            "INSERT INTO customers (UserId, UserType, Name, Address, Number)" \
            " VALUES ({0}, \'{1}\', \'{2}\', \'{3}\', \'{4}\') ON CONFLICT DO NOTHING".format(user_id, user_type, name,
                                                                                              address, number),
        )
        return

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
            "SELECT * FROM orders WHERE customerid = $1",
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
        await self.conn.execute(
            "INSERT INTO couriers(UserId, Name, Number, PassportMain, PassportRegistration, DriverLicenseFront, DriverLicenseBack) "
            "VALUES ({0}, \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\', \'{6}\')".format(user_id,
                                                                                        name,
                                                                                        number,
                                                                                        passport_main_id,
                                                                                        passport_registration_id,
                                                                                        driver_license_front_id,
                                                                                        driver_license_back_id)
        )

    async def get_couriers_list(self):
        """Get couriers list"""
        rows = await self.conn.fetch(
            "SELECT userid FROM couriers"
        )
        return [dict(row) for row in rows]

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
        result = self.conn.fetchrow(
            "SELECT * FROM orders WHERE orderid = $1",
            order_id
        )
        return result

    async def change_order_status(self, order_id: int, order_status: str):
        """Change order status by order_id"""
        await self.conn.execute(
            f"UPDATE orders SET status = \'{order_status}\' WHERE orderid = {order_id}"
        )

    # stats
    async def get_orders_count(self, date_range: str):
        """Get orders count by date range"""
        result = self.conn.fetchval(
            """select date_trunc('$1', orders.CurrentTime), count(1) from orders group by 1;""",
            date_range
        )
        return result
