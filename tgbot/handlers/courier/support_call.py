from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline.courier.support import support_keyboard, check_support_available, get_support_manager, \
    cancel_support
from tgbot.services.repository import Repo


async def ask_support_call_callback(c: CallbackQuery, repo: Repo, state: FSMContext):
    text = "Хотите связаться с техподдержкой? Нажмите на кнопку ниже!"
    customer_data = await repo.get_customer(user_id=c.message.chat.id)
    keyboard = await support_keyboard(messages="many", state=state, user_id=c.message.chat.id, city=customer_data['city'], repo=repo)
    if not keyboard:
        await c.message.answer("К сожалению, сейчас нет свободных операторов. Попробуйте позже.")
        return
    await c.message.answer(text=text, reply_markup=keyboard)
    await c.answer()


async def ask_support_call(m: Message, repo: Repo, state: FSMContext):
    text = "Хотите связаться с техподдержкой? Нажмите на кнопку ниже!"
    courier_data = await repo.get_courier(courier_id=m.chat.id)
    keyboard = await support_keyboard(messages="many", state=state, city=courier_data['city'], repo=repo)
    if not keyboard:
        await m.answer("К сожалению, сейчас нет свободных операторов. Попробуйте позже.")
        return
    await m.answer(text=text, reply_markup=keyboard)


async def send_to_support_call(c: CallbackQuery, state: FSMContext, callback_data: dict, repo: Repo):
    await c.message.edit_text("Вы обратились в техподдержку. Ждем ответа от оператора!")

    user_id = int(callback_data.get("user_id"))
    courier_data = await repo.get_courier(courier_id=c.from_user.id)
    if not await check_support_available(user_id, state=state):
        support_id = await get_support_manager(state=state, repo=repo, city=courier_data['city'])
    else:
        support_id = user_id

    if not support_id:
        await c.message.edit_text("К сожалению, сейчас нет свободных операторов. Попробуйте позже.")
        await state.reset_state()
        return

    await state.set_state("wait_in_support")
    await state.update_data(second_id=support_id)

    keyboard = await support_keyboard(messages="many", user_id=c.from_user.id, state=state, city=courier_data['city'], repo=repo)

    courier_data = await repo.get_courier(courier_id=c.from_user.id)
    await c.bot.send_message(support_id,
                             f"С вами хочет связаться курьер <b>№{courier_data['id']} {c.from_user.full_name}</b>",
                             reply_markup=keyboard
                             )


async def answer_support_call(c: CallbackQuery, state: FSMContext, callback_data: dict, repo: Repo):
    second_id = int(callback_data.get("user_id"))
    user_state = await state.storage.get_state(user=second_id, chat=second_id)

    if str(user_state) != "wait_in_support":
        await c.message.edit_text("К сожалению, пользователь уже передумал.")
        return

    await state.set_state("in_support")
    await state.storage.set_state(user=second_id, chat=second_id, state="in_support")

    await state.update_data(second_id=second_id)

    keyboard = cancel_support(second_id)
    keyboard_second_user = cancel_support(c.from_user.id)

    courier_data = await repo.get_courier(courier_id=second_id)

    await c.message.edit_text(f"Вы на связи с курьером <b>№{courier_data['id']} {courier_data['name']}</b>!\n"
                              "Чтобы завершить общение нажмите на кнопку в закрепленном сообщении.",
                              reply_markup=keyboard
                              )
    await c.message.pin()
    support_message = await c.bot.send_message(second_id,
                                               "Тех. поддержка на связи! Можете писать сюда свое сообщение. \n"
                                               "Чтобы завершить общение нажмите на кнопку в закрепленном сообщении.",
                                               reply_markup=keyboard_second_user
                                               )
    await c.bot.pin_chat_message(chat_id=second_id, message_id=support_message.message_id)


async def not_supported(m: Message, state: FSMContext):
    data = await state.get_data()
    second_id = data.get("second_id")

    keyboard = cancel_support(second_id)
    await m.answer("Дождитесь ответа оператора или отмените сеанс", reply_markup=keyboard)


async def exit_support(c: CallbackQuery, state: FSMContext, callback_data: dict):
    user_id = int(callback_data.get("user_id"))
    second_state = await state.storage.get_data(chat=user_id, user=user_id)

    if len(second_state) > 0:
        second_id = second_state.get("second_id")
        if int(second_id) == c.from_user.id:
            await state.storage.reset_state(chat=user_id, user=user_id)
            await c.bot.send_message(user_id, "Сеанс тех. поддержки завершен.")
        await c.bot.unpin_all_chat_messages(chat_id=second_id)
        await c.bot.unpin_all_chat_messages(chat_id=user_id)

    await c.message.edit_text("Вы завершили сеанс")
    await state.reset_state()
