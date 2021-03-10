from aiogram.types import Message

from tgbot.keyboards.default.user.return_to_menu import return_to_menu


async def tech_support(m: Message):
    await m.reply(text="""*Техподдержка MEGABOT*
EMail: megabot\_flowers@mail\.ru
Telegram: @MegaBot\_flowers
WhatsApp: \+79881739293 \([Перейти](https://wa.me/79881739293)\)
Телефон: 43\-92\-93""",
                  reply_markup=return_to_menu,
                  parse_mode="MARKDOWNV2",
                  disable_web_page_preview=True)
