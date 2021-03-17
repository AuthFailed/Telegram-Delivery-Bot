from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from tgbot.config import load_config
from tgbot.models.role import UserRole


class RoleMiddleware(LifetimeControllerMiddleware):
    def __init__(self, admin_id: int):
        super().__init__()
        self.admin_id = admin_id

    async def pre_process(self, obj, data, *args):
        repo = data['repo']
        couriers_list = [courier['userid'] for courier in await repo.get_couriers_list()]
        config = load_config('bot.ini')
        managers_list = config.tg_bot.managers
        if not hasattr(obj, "from_user"):
            data["role"] = None
        elif obj.from_user.id == self.admin_id:
            data["role"] = UserRole.ADMIN
        elif str(obj.from_user.id) in managers_list:
            data["role"] = UserRole.MANAGER
        elif obj.from_user.id in couriers_list:
            data["role"] = UserRole.COURIER
        else:
            data["role"] = UserRole.USER

    async def post_process(self, obj, data, *args):
        del data["role"]
