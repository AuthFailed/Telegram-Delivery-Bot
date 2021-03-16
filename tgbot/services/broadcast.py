import asyncio

from aiogram import Bot
from aiogram.utils import exceptions

from bot import logger
from tgbot.services.repository import Repo


async def send_photo(bot: Bot, repo: Repo, user_id: int, photo, caption: str,
                     disable_notification: bool = False):
    """
    Безопасная рассылка
    :param repo:
    :param bot:
    :param caption:
    :param photo:
    :param user_id:
    :param disable_notification:
    :return:
    """
    try:
        await bot.send_photo(chat_id=user_id, photo=photo, caption=caption, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        logger.error(f"Пользователь [ID:{user_id}]: Бот заблокирован пользователем")
        await repo.delete_customer(user_id)
    except exceptions.ChatNotFound:
        logger.error(f"Пользователь [ID:{user_id}]: Неверный ID пользователя")
    except exceptions.RetryAfter as e:
        logger.error(f"Пользователь [ID:{user_id}]: Достигнут лимит рассылки. Засыпаю на {e.timeout} секунд.")
        await asyncio.sleep(e.timeout)
        return await send_photo(user_id, photo, caption)  # Recursive call
    except exceptions.UserDeactivated:
        logger.error(f"Пользователь [ID:{user_id}]: Аккаунт деактивирован/удалён")
    except exceptions.TelegramAPIError:
        logger.exception(f"Пользователь [ID:{user_id}]: Провалено")
    except exceptions.BotKicked:
        logger.exception(f"Бот был удален из группы. Удаляю [ID:{user_id}] из базы")
        await repo.delete_customer(user_id)
    else:
        logger.info(f"Пользователь [ID:{user_id}]: Успешно")
