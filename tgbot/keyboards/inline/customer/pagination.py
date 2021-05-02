from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.customer.callback_data import show_item_data, pagination_call, show_partner_data, \
    show_manager_data, registration_city, show_courier_data


async def get_pages_keyboard(array, width: int = 1, items_per_page: int = 5, page: int = 1, key: str = "items"):
    markup = InlineKeyboardMarkup(row_width=width)

    MAX_ITEMS_PER_PAGE = items_per_page
    first_item_index = (page - 1) * MAX_ITEMS_PER_PAGE
    last_item_index = page * MAX_ITEMS_PER_PAGE

    sliced_array = array[first_item_index:last_item_index]
    item_buttons = list()

    if key == "partners":
        for item in sliced_array:
            item_buttons.append(
                InlineKeyboardButton(
                    text=f'№{item["id"]} | {item["city"].title()} | {"✅️" if item["working"] else "❌"}',
                    callback_data=show_partner_data.new(partner_id=item['adminid'])
                ))
    elif key == "managers":
        for item in sliced_array:
            item_buttons.append(
                InlineKeyboardButton(
                    text=f'№{item["id"]} | {item["name"]}',
                    callback_data=show_manager_data.new(manager_id=item['userid'])
                ))
    elif key == "couriers":
        for item in sliced_array:
            item_buttons.append(
                InlineKeyboardButton(
                    text=f'№{item["id"]} {item["name"]} | ⏳ {item["status"]}',
                    callback_data=show_courier_data.new(courier_id=item['userid'])
                ))
    elif key == "items":
        for item in sliced_array:
            item_buttons.append(
                InlineKeyboardButton(
                    text=f'№{item["id"]} | ⏳ {item["status"]}',
                    callback_data=show_item_data.new(item_id=item['id'])
                ))
    elif key == "cities":
        for item in sliced_array:
            item_buttons.append(
                InlineKeyboardButton(
                    text=f'{item["city"].title()}',
                    callback_data=registration_city.new(city_name=item["city"])
                ))

    pages_buttons = list()
    first_page = 1
    first_page_text = "« 1"

    if len(array) % MAX_ITEMS_PER_PAGE == 0:
        max_page = len(array) // MAX_ITEMS_PER_PAGE
    else:
        max_page = len(array) // MAX_ITEMS_PER_PAGE + 1

    max_page_text = f"» {max_page}"

    pages_buttons.append(
        InlineKeyboardButton(
            text=first_page_text,
            callback_data=pagination_call.new(key=key, page=first_page)
        )
    )

    previous_page = page - 1
    previous_page_text = f'< {previous_page}'

    if previous_page >= first_page:
        pages_buttons.append(
            InlineKeyboardButton(
                text=previous_page_text,
                callback_data=pagination_call.new(key=key, page=previous_page)
            )
        )
    else:
        pages_buttons.append(
            InlineKeyboardButton(
                text=" . ",
                callback_data=pagination_call.new(key=key, page="current_page")
            )
        )

    pages_buttons.append(
        InlineKeyboardButton(
            text=f' 📓 {page} ',
            callback_data=pagination_call.new(key=key, page="current_page")
        )
    )

    next_page = page + 1
    next_page_text = f'{next_page} >'

    if next_page <= max_page:
        pages_buttons.append(
            InlineKeyboardButton(
                text=next_page_text,
                callback_data=pagination_call.new(key=key, page=next_page)
            )
        )
    else:
        pages_buttons.append(
            InlineKeyboardButton(
                text=" . ",
                callback_data=pagination_call.new(key=key, page="current_page")
            )
        )

    pages_buttons.append(
        InlineKeyboardButton(
            text=max_page_text,
            callback_data=pagination_call.new(key=key, page=max_page)
        )
    )

    for button in item_buttons:
        markup.insert(button)

    if key == "partners":
        markup.add(
            InlineKeyboardButton(
                text="👨 Добавить партнера",
                callback_data=show_partner_data.new(partner_id="add")
            )
        )
    elif key == "managers":
        markup.add(
            InlineKeyboardButton(
                text="👨‍💼 Добавить менеджера",
                callback_data=show_manager_data.new(manager_id="add")
            )
        )
    elif key == "couriers":
        markup.add(
            InlineKeyboardButton(
                text="👨‍💼 Добавить курьера",
                callback_data=show_courier_data.new(courier_id="add")
            )
        )

    markup.row(*pages_buttons)
    return markup
