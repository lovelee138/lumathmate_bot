import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from handlers import authorization, commands, send_note, get_note, add_new_stud
from db import load_config
import logging


dp = Dispatcher()


async def main():
    BOT_TOKEN = load_config(filename="config/bot.ini", section="bot")["token"]
    bot = Bot(BOT_TOKEN)

    logging.basicConfig(level=logging.INFO)

    dp.include_routers(authorization.router)
    dp.include_routers(commands.router)
    dp.include_routers(send_note.router)
    dp.include_routers(get_note.router)
    dp.include_router(add_new_stud.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
