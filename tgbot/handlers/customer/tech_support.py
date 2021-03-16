from aiogram.types import Message

from tgbot.keyboards.default.user.return_to_menu import return_to_menu


async def tech_support(m: Message):
    await m.reply(text="""<b>Техподдержка MEGABOT</b>
EMail: megabot_flowers@mail.ru
Telegram: @MegaBot_flowers
WhatsApp: +79881739293 (<a href='https://wa.me/79881739293'>Перейти</a>)
Телефон: 43-92-93""",
                  reply_markup=return_to_menu,
                  disable_web_page_preview=True)
