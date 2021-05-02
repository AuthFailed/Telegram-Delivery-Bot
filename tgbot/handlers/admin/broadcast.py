from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram_dialog import DialogManager, Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Group, Button, Next, Url, Back
from aiogram_dialog.widgets.text import Const, Format

from tgbot.keyboards.default.admin.broadcast import broadcast
from tgbot.services.broadcast import send_photo
from tgbot.services.repository import Repo
from tgbot.states.admin.post import Broadcast, types_kbd, get_data, get_text, get_image


async def on_finish(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.done()
    await c.message.edit_text("Рассылка отменена!")


async def broadcast_text(m: Message, dialog: Dialog, manager: DialogManager):
    if len(m.html_text) <= 4096:
        await manager.start(Broadcast.broadcast_text, m.html_text, reset_stack=False)
    else:
        await m.answer(text="Ваш текст превышает максимальное кол-во символов (4096)!")


async def broadcast_image(m: Message, dialog: Dialog, manager: DialogManager):
    if m.content_type['PHOTO']:
        print("оп у нас тут фоточка образовалась")
        await manager.start(Broadcast.broadcast_image, m.photo[0].file_id, reset_stack=False)
    else:
        await m.answer(text="Прикрепите фотографию")


broadcast = Dialog(
    Window(
        Format("<b>Следующие роли получат рассылку:</b>"
               "\n• {selected}"),
        types_kbd,
        Group(Button(Const("Отмена"), id="Cancel", on_click=on_finish),
              Next(Const("Далее")), width=2, keep_rows=False),
        getter=get_data,
        state=Broadcast.broadcast_type,
    ),
    Window(
        Format("<b>Следующие роли получат рассылку:</b>"
               "\n• {selected}"
               "\n\n<b>Текст рассылаемого сообщения:</b>"
               "\n{text}"
               "\n\n<i>Поддерживается встроенное в Telegram форматирование!"
               "\nМаксимальное кол-во символов: 4096</i>"),
        Url(Const("Про форматирование"), Const("https://lifehacker.ru/formatirovanie-teksta-v-telegram/")),
        Button(Const("Отмена"), id="Cancel", on_click=on_finish),
        Group(Back(Const("Назад")), Next(Const("Далее")), width=2, keep_rows=False),
        MessageInput(broadcast_text),
        getter=get_text,
        state=Broadcast.broadcast_text,
    ),
    Window(
        Format("<b>Если хотите прикрепить фотографию к вашей рассылке, пришлите ее на этом этапе:</b>\n"
               "{image_id}"),
        MessageInput(broadcast_image),
        Button(Const("Отмена"), id="Cancel", on_click=on_finish),
        Group(Back(Const("Назад")), Next(Const("Далее")), width=2, keep_rows=False),
        getter=get_image,
        state=Broadcast.broadcast_image
    ))  # @TODO починить выбор картинки


async def broadcast_start(m: Message, repo: Repo, dialog_manager: DialogManager):
    await dialog_manager.start(Broadcast.broadcast_type, reset_stack=True)


async def broadcast_image(m: Message, state: FSMContext):
    async with state.proxy() as data:
        data['media'] = m.photo[0].file_id

    await m.reply(text='Отправляем?', reply_markup=broadcast)
    await Post.next()


async def broadcast_choice(m: Message, repo: Repo, state: FSMContext):
    if m.text == "✉️ Отправить":
        city_info = await repo.get_partner(userid=m.chat.id)
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
