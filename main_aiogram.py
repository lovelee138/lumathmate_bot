import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from db_actions import *


BOT_TOKEN = load_config(filename="config/bot.ini", section="bot")["token"]

HELP_COMMAND = """
/start - начало
/help - список комманд
/info - информация о боте

/get_note - получить последний конспект
"""

START_MESSAGE = """
Привет! Я твой помощник в изучении математики!
Нажми /help, чтобы увидеть список всех доступных комманд.

Удачи в обучении! ❤️
"""

INFO_MESSAGE = """
Я бот-помощник в изучении математики!
Я создан для того, чтобы удобно организовать учебный процесс, а именно поиск и получение нужного конспекта, отправка дз, ее обсуждение, тренировка определенных тем.
Нажми /help, чтобы увидеть список комманд.
"""


bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def help_command(message: types.message):
    await message.answer(START_MESSAGE)
    await message.delete()


@dp.message(Command("help"))
async def help_command(message: types.message):
    await message.answer(HELP_COMMAND)
    await message.delete()


@dp.message(Command("info"))
async def help_command(message: types.message):
    await message.answer(INFO_MESSAGE)
    await message.delete()


@dp.message(Command("get_note"))
async def help_command(message: types.message):
    note_name = get_last_note(message.from_user.id)
    note = FSInputFile(f"notes/{note_name}")
    await bot.send_document(chat_id=message.from_user.id, document=note)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
