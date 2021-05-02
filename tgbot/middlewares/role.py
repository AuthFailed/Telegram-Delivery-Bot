from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from tgbot.models.role import UserRole


class RoleMiddleware(LifetimeControllerMiddleware):
    def __init__(self):
        super().__init__()

    async def pre_process(self, obj, data, *args):
        repo = data['repo']
        admins_list = [partner["adminid"] for partner in await repo.get_partners(with_main=True)]
        couriers_list = [courier['userid'] for courier in await repo.get_couriers_list()]
        managers_list = [manager['userid'] for manager in await repo.get_managers_list()]
        if not hasattr(obj, "from_user"):
            data["role"] = None
        elif str(obj.from_user.id) in admins_list:
            data["role"] = UserRole.ADMIN
        elif str(obj.from_user.id) in managers_list:
            data["role"] = UserRole.MANAGER
        elif str(obj.from_user.id) in couriers_list:
            data["role"] = UserRole.COURIER
        else:
            data["role"] = UserRole.USER
        print(data["role"])

    async def post_process(self, obj, data, *args):
        del data["role"]
