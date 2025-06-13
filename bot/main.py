import os
import logging
import asyncio

from aiogram import Bot, Dispatcher
from handlers import router


bot = Bot(os.getenv("BOT_TOKEN"))
dispatcher = Dispatcher()
dispatcher.include_router(router)


async def main():
    logging.info("Бот запущен")
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
