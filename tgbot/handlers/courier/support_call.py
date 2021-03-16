from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline.courier.support import support_keyboard, check_support_available, get_support_manager, \
    cancel_support


async def ask_support_call(message: Message, state: FSMContext):
    text = "Хотите связаться с техподдержкой? Нажмите на кнопку ниже!"
    keyboard = await support_keyboard(messages="many", state=state)
    if not keyboard:
        await message.answer("К сожалению, сейчас нет свободных операторов. Попробуйте позже.")
        return
    await message.answer(text, reply_markup=keyboard)


async def send_to_support_call(c: CallbackQuery, state: FSMContext, callback_data: dict):
    await c.message.edit_text("Вы обратились в техподдержку. Ждем ответа от оператора!")

    user_id = int(callback_data.get("user_id"))
    if not await check_support_available(user_id, state=state):
        support_id = await get_support_manager(state=state)
    else:
        support_id = user_id

    if not support_id:
        await c.message.edit_text("К сожалению, сейчас нет свободных операторов. Попробуйте позже.")
        await state.reset_state()
        return

    await state.set_state("wait_in_support")
    await state.update_data(second_id=support_id)

    keyboard = await support_keyboard(messages="many", user_id=c.from_user.id, state=state)

    await c.bot.send_message(support_id,
                             f"С вами хочет связаться пользователь {c.from_user.full_name}",
                             reply_markup=keyboard
                             )


async def answer_support_call(c: CallbackQuery, state: FSMContext, callback_data: dict):
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

    await c.message.edit_text("Вы на связи с пользователем!\n"
                              "Чтобы завершить общение нажмите на кнопку.",
                              reply_markup=keyboard
                              )
    await c.bot.send_message(second_id,
                             "Техподдержка на связи! Можете писать сюда свое сообщение. \n"
                             "Чтобы завершить общение нажмите на кнопку.",
                             reply_markup=keyboard_second_user
                             )


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
            await c.bot.send_message(user_id, "Пользователь завершил сеанс техподдержки")

    await c.message.edit_text("Вы завершили сеанс")
    await state.reset_state()
