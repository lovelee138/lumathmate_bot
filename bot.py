import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from handlers import commands, authorization
from db_actions import *


dp = Dispatcher()


async def main():
    BOT_TOKEN = load_config(filename="config/bot.ini", section="bot")["token"]
    bot = Bot(BOT_TOKEN)

    dp.include_routers(authorization.router)
    dp.include_routers(commands.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())
