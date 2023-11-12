import logging
import sys
import asyncio
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from storage import Storage

bot_token = getenv("ERBAUER_BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

storage = Storage()
# dp = Dispatcher()
#
#
# async def main() -> None:
#     bot = Bot(bot_token, parse_mode=ParseMode.HTML)
#     try:
#         await dp.start_polling(bot)
#     finally:
#         storage.close_connection()
#
#
# if __name__ == '__main__':
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())
    