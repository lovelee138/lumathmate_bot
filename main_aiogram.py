from aiogram import Bot, Dispatcher, executor, types
from db_actions import *


BOT_TOKEN = load_config(filename="config/bot.ini", section="bot")["token"]

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    print("I've been started!")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
