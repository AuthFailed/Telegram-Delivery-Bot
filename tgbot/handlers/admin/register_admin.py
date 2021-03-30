from aiogram import Dispatcher
from aiogram.types import ChatType

from tgbot.handlers.admin.broadcast import broadcast_text, broadcast_start, broadcast_image, broadcast_choice
from tgbot.handlers.admin.get_courier import get_courier
from tgbot.handlers.admin.get_customer import get_customer
from tgbot.handlers.admin.get_order import get_order
from tgbot.handlers.admin.manage_bot import manage_bot
from tgbot.handlers.admin.managers_interaction import list_of_available_managers, show_chosen_page_managers, \
    manager_action, add_manager, show_manager, manager_id, manager_fio, manager_number, manager_choice
from tgbot.handlers.admin.partners_interaction import list_of_available_partners, show_chosen_page_partners, add_partner, \
    show_partner, partner_action, partner_city, partner_id, partner_choice
from tgbot.handlers.admin.servers_stats import servers_stats
from tgbot.handlers.admin.setting_groups import setting_groups
from tgbot.handlers.admin.start import start
from tgbot.keyboards.inline.admin.callback_data import partner, manager
from tgbot.keyboards.inline.customer.callback_data import pagination_call, show_partner_data, show_manager_data
from tgbot.states.admin.new_manager import NewManager
from tgbot.states.admin.new_partner import NewPartner
from tgbot.states.admin.post import Post


def register_admin(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start", "menu"], is_admin=True, chat_type=ChatType.PRIVATE)
    dp.register_message_handler(start, text="🏠 Вернуться в меню", state="*", is_admin=True, chat_type=ChatType.PRIVATE)

    # @TODO Управление партнерами
    dp.register_message_handler(list_of_available_partners, text="🤝 Партнеры", is_admin=True, chat_type=ChatType.PRIVATE)
    dp.register_callback_query_handler(show_chosen_page_partners, pagination_call.filter(key="partners"))
    dp.register_callback_query_handler(partner_action, partner.filter())
    dp.register_callback_query_handler(add_partner, show_partner_data.filter(partner_id="add"))
    dp.register_callback_query_handler(show_partner, show_partner_data.filter())
    dp.register_message_handler(partner_city, state=NewPartner.city, is_admin=True, chat_type=ChatType.PRIVATE)
    dp.register_message_handler(partner_id, state=NewPartner.admin_id, is_admin=True, chat_type=ChatType.PRIVATE)
    dp.register_message_handler(partner_choice, state=NewPartner.choice, is_admin=True, chat_type=ChatType.PRIVATE)

    # Управление менеджерами
    dp.register_message_handler(list_of_available_managers, text="👨‍💼 Менеджеры", is_admin=True,
                                chat_type=ChatType.PRIVATE)
    dp.register_callback_query_handler(show_chosen_page_managers, pagination_call.filter(key="managers"))
    dp.register_callback_query_handler(manager_action, manager.filter())

    dp.register_callback_query_handler(add_manager, show_manager_data.filter(manager_id="add"))
    dp.register_callback_query_handler(show_manager, show_manager_data.filter())
    dp.register_message_handler(manager_id, state=NewManager.manager_id, is_admin=True, chat_type=ChatType.PRIVATE)
    dp.register_message_handler(manager_fio, state=NewManager.fio, is_admin=True, chat_type=ChatType.PRIVATE)
    dp.register_message_handler(manager_number, state=NewManager.number, is_admin=True, chat_type=ChatType.PRIVATE)
    dp.register_message_handler(manager_choice, state=NewManager.choice, is_admin=True, chat_type=ChatType.PRIVATE)

    # @TODO Управление курьерами

    # Управление ботом
    dp.register_message_handler(manage_bot, text="🤖 Управление ботом", chat_type=ChatType.PRIVATE)

    # Рассылка
    dp.register_message_handler(broadcast_start, text="📢 Рассылка", is_admin=True, chat_type=ChatType.PRIVATE)
    dp.register_message_handler(broadcast_text, state=Post.text, is_admin=True,
                                chat_type=ChatType.PRIVATE)
    dp.register_message_handler(broadcast_image, state=Post.media, content_types=['photo'], is_admin=True,
                                chat_type=ChatType.PRIVATE)
    dp.register_message_handler(broadcast_choice, state=Post.choice, is_admin=True,
                                chat_type=ChatType.PRIVATE)

    # Остальные команды
    dp.register_message_handler(servers_stats, text="⚙️ Статус сервера", is_admin=True, chat_type=ChatType.PRIVATE)
    dp.register_message_handler(setting_groups, commands=["setting_groups"], is_admin=True, chat_type=ChatType.PRIVATE)

    dp.register_message_handler(get_courier, commands=["курьер"], is_admin=True, chat_type=ChatType.PRIVATE)
    dp.register_message_handler(get_order, commands=["заказ"], is_admin=True, chat_type=ChatType.PRIVATE)
    dp.register_message_handler(get_customer, commands=["заказчик"], is_admin=True, chat_type=ChatType.PRIVATE)
