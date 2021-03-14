# change order courier
from aiogram.types import CallbackQuery, Message
from tgbot.handlers.admin.order_interaction import generate_order_data_message

from tgbot.handlers.customer.personal_profile import personal_profile
from tgbot.keyboards.default.user.personal_profile import personal_profile_kb
from tgbot.keyboards.inline.customer.orders import my_orders_kb
from tgbot.services.repository import Repo


async def list_of_available_orders(m: Message, repo: Repo):
    user_orders = await repo.get_user_orders(user_id=m.chat.id)
    await m.answer(text="Ваши заказы:",
                   reply_markup=await my_orders_kb(user_orders))


async def get_order_info(call: CallbackQuery, callback_data: dict, repo: Repo):
    order_id = callback_data['order_id']
    if callback_data['order_id'] == "Вернуться":
        await call.message.answer(text=await personal_profile(m=call.message, repo=repo),
                                  reply_markup=personal_profile_kb,
                                  parse_mode="Markdown")
    else:
        choosed_courier_id = callback_data['order_id']

        await repo.change_order_courier(order_id=order_id, courier_id=choosed_courier_id)
        await call.bot.send_message(chat_id=call.message.chat.id,
                                    text=await generate_order_data_message(order_id=order_id, repo=repo),
                                    parse_mode="Markdown",
                                    reply_markup=personal_profile_kb)
        await call.answer(text=f"Информация о заказе №{order_id}")
