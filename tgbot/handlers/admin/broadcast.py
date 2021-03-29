from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from tgbot.keyboards.default.admin.broadcast import broadcast
from tgbot.keyboards.default.admin.return_to_menu import return_to_menu
from tgbot.services.broadcast import send_photo
from tgbot.services.repository import Repo
from tgbot.states.admin.post import Post


async def broadcast_start(m: Message, repo: Repo):
    await m.reply(text="""📜 <b>Введите рассылаемый текст:</b>

<i>Подсказка: Текст поддерживает форматирование.
На данный момент поддерживается рассылка только заказчикам.</i>""",
                  reply_markup=return_to_menu,
                  disable_web_page_preview=True)
    await Post.first()


async def broadcast_text(m: Message, state: FSMContext):
    await state.update_data(text=m.html_text)

    await m.reply(text="🖼️ Теперь пришли мне картинку:")
    await Post.next()


async def broadcast_image(m: Message, state: FSMContext):
    async with state.proxy() as data:
        data['media'] = m.photo[0].file_id

    await m.reply(text='Отправляем?', reply_markup=broadcast)
    await Post.next()


async def broadcast_choice(m: Message, repo: Repo, state: FSMContext):
    if m.text == "✉️ Отправить":
        city_info = await repo.get_partner(admin_id=m.chat.id)
        customers_list = await repo.get_customers_list(city_name=city_info['city'])
        broadcast_data = await state.get_data()
        i = 0
        for customer in customers_list:
            await send_photo(bot=m.bot, repo=repo, user_id=customer["userid"], photo=broadcast_data['media'],
                             caption=broadcast_data['text'])
            i += 1
        await state.finish()
        await m.answer(
            text=f"Рассылка завершена!\nСообщений разослано: <b>{i}</b>", reply_markup=ReplyKeyboardRemove()
        )
