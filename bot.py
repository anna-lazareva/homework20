import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# Определите свой токен
bot_token = getenv("MY_BOT_TOKEN")
if not bot_token:
    logging.error("Ошибка: токен не предоставлен.")
    exit()


class TelegramBot:
    """
    Класс, представляющий телеграм-бота.

    Attributes:
        bot (Bot): Объект бота для взаимодействия с Telegram API.
        dp (Dispatcher): Объект диспетчера для обработки сообщений и команд.
    """
    
    def __init__(self, api_token):
        """
        Инициализация объекта телеграм-бота.

        Args:
            api_token (str): Токен для доступа к API Telegram.
        """
        self.dp = Dispatcher()
        self.bot = Bot(token=api_token, parse_mode=ParseMode.HTML)
        self.bot.get
  
    async def start_polling(self):
        """
        Запускает пулинг для получения сообщений от пользователей.
        """
        await self.dp.start_polling(self.bot)
        
    async def send_message(self, message):
        """
        Отправляем сообщение.
        
        Args:
            message (str): сообщение.
        """
        await self.bot.send_message(self.bot)


async def main() -> None:
    bot = TelegramBot(bot_token)
    
    # Текст пригласительного сообщения
    invite_message = (
        "Что может этот бот?\n\n"
        "✅ Бла-бла-бла.\n"
        "✅ Бла-бла-бла.\n"
        "✅ Бла-бла-бла.\n"
        "✅ ...\n"
        "Нажмите Старт 👇 чтобы войти!"
    )

    # Отправка приветственного сообщения
    await bot.send_message(invite_message)
    
    await bot.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
