"""
8D Audio Bot - ishga tushirish fayli.

Ishga tushirish:
    python main.py
"""

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from handlers import router


def setup_logging():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ],
    )

    logging.getLogger("aiogram.event").setLevel(
        logging.WARNING
    )



async def main():

    setup_logging()

    logger = logging.getLogger(__name__)


    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        ),
    )


    dp = Dispatcher(
        storage=MemoryStorage()
    )


    dp.include_router(router)


    try:

        logger.info("Bot ishga tushmoqda...")


        # Eski webhook/update larni tozalash
        await bot.delete_webhook(
            drop_pending_updates=True
        )


        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types()
        )


    except Exception as e:

        logger.exception(
            "Bot xatosi: %s",
            e
        )


    finally:

        await bot.session.close()

        logger.info(
            "Bot to'xtatildi."
        )



if __name__ == "__main__":

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        print(
            "\nBot foydalanuvchi tomonidan to'xtatildi."
        )