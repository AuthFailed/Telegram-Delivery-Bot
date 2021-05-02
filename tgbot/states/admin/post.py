import operator
from datetime import datetime

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Multiselect
from aiogram_dialog.widgets.text import Format


class Broadcast(StatesGroup):
    broadcast_type = State()
    broadcast_text = State()
    broadcast_image = State()
    broadcast_choice = State()


async def get_data(dialog_manager: DialogManager, **kwargs):
    types = [
        ("👨‍💼 Менеджеры", 'managers'),
        ("🚚 Курьеры", 'couriers'),
        ("🛍 Заказчики", 'customers')
    ]
    selected = await get_selected(dialog_manager)
    return {
        "selected": selected["selected"] if len(selected) > 0 else "Используйте кнопки",
        "types": types,
        "count": len(types)
    }


async def get_selected(dialog_manager: DialogManager, **kwargs):
    return {"selected": "\n• ".join(types_kbd.find(widget_id="m_types").get_checked(dialog_manager))
        .replace('couriers', '🚚 Курьеры')
        .replace('managers', '👨‍💼 Менеджеры')
        .replace('customers', '🛍 Заказчики')}


async def get_text(dialog_manager: DialogManager, **kwargs):
    selected = await get_selected(dialog_manager)
    text = dialog_manager.current_intent().data
    return {
        "selected": selected["selected"],
        "text": text if text is not None else "Отправьте мне текст рассылки",
        "now": datetime.now().isoformat(),
    }


async def get_image(dialog_manager: DialogManager, **kwargs):
    image_id = dialog_manager.current_intent().data
    return {
        "image_id": image_id if image_id is not None else "Прикрепите фотографию"
    }


types_kbd = Multiselect(
    Format("✓ {item[0]}"), Format("{item[0]}"),
    id="m_types",
    item_id_getter=operator.itemgetter(1),
    min_selected=1,
    items="types",
)
