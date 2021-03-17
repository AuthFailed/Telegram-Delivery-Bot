from aiogram import Dispatcher
from aiogram.types import ChatType

from tgbot.handlers.admin.broadcast import broadcast_text, broadcast_start, broadcast_image, broadcast_choice
from tgbot.handlers.admin.get_courier import get_courier
from tgbot.handlers.admin.get_customer import get_customer
from tgbot.handlers.admin.get_order import get_order
from tgbot.handlers.admin.manage_bot import manage_bot
from tgbot.handlers.admin.servers_stats import servers_stats
from tgbot.handlers.admin.start import start
from tgbot.models.role import UserRole
from tgbot.states.admin.post import Post


def register_admin(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start", "menu"], is_admin=True, chat_type=ChatType.PRIVATE)
    dp.register_message_handler(start, text="🏠 Вернуться в меню", state="*", is_admin=True, chat_type=ChatType.PRIVATE)

    # @TODO Статистика

    # @TODO Управление курьерами

    # Управление ботом
    dp.register_message_handler(manage_bot, text="🤖 Управление ботом", is_admin=True, chat_type=ChatType.PRIVATE)

    dp.register_message_handler(broadcast_start, text="📢 Рассылка", is_admin=True, chat_type=ChatType.PRIVATE)
    dp.register_message_handler(broadcast_text, state=Post.text, is_admin=True, content_types=['text'],
                                chat_type=ChatType.PRIVATE)
    dp.register_message_handler(broadcast_image, state=Post.media, content_types=['photo'], is_admin=True,
                                chat_type=ChatType.PRIVATE)
    dp.register_message_handler(broadcast_choice, state=Post.choice, content_types=['text'], is_admin=True,
                                chat_type=ChatType.PRIVATE)

    dp.register_message_handler(servers_stats, text="⚙️ Статус сервера", is_admin=True, chat_type=ChatType.PRIVATE)

    dp.register_message_handler(get_courier, commands=["курьер"], is_admin=True, chat_type=ChatType.PRIVATE)

    # Get order info
    dp.register_message_handler(get_order, commands=["заказ"], is_admin=True, chat_type=ChatType.PRIVATE)

    # Get customer new_info
    dp.register_message_handler(get_customer, commands=["заказчик"], is_admin=True, chat_type=ChatType.PRIVATE)
