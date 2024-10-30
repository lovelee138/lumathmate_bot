import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from handlers import authorization, commands, send_note, get_note
from db_actions import *
import logging


dp = Dispatcher()


async def main():
    BOT_TOKEN = load_config(filename="config/bot.ini", section="bot")["token"]
    bot = Bot(BOT_TOKEN)

    logging.basicConfig(level=logging.INFO)

    start_kb = [[KeyboardButton(text="/start")]]
    kb = ReplyKeyboardMarkup(keyboard=start_kb, resize_keyboard=True)

    dp.include_routers(authorization.router)
    dp.include_routers(commands.router)
    dp.include_routers(send_note.router)
    dp.include_routers(get_note.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())
