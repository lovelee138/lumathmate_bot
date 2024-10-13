import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db_actions import *


BOT_TOKEN = load_config(filename="config/bot.ini", section="bot")["token"]

HELP_COMMAND = """
/start - регистрация в боте
/help - список комманд
/info - информация о боте

/get_note - получить последний конспект
"""

START_MESSAGE = """
Привет! Я твой помощник в изучении математики!
Сначала тебе нужно зарегистрироваться в сервисе.
"""

INFO_MESSAGE = """
Я бот-помощник в изучении математики!
Я создан для того, чтобы удобно организовать учебный процесс, а именно поиск и получение нужного конспекта, отправка дз, ее обсуждение, тренировка определенных тем.

Нажми /help, чтобы увидеть список комманд.
"""


bot = Bot(BOT_TOKEN)
dp = Dispatcher()


# Callback functions

@dp.callback_query(F.data == "student_authorization")
async def authorize_student(callback: types.CallbackQuery):
    user_id = callback.message.from_user.id

    student_signed = is_signed_up(user_id, "student")
    if not student_signed:
        await callback.message.answer("Введите Ваш идентификатор, выданный преподавателем или идентификатор преподавателя.")
    else:
        await callback.message.answer("Вы", *student_signed)

    await callback.answer()


@dp.callback_query(F.data == "teacher_authorization")
async def authorize_teacher(callback: types.CallbackQuery):
    await callback.message.answer("вы заебавшийся препод")
    await callback.answer()


# Command functions

@dp.message(Command("start"))
async def help_command(message: types.message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Я ученик",
        callback_data="student_authorization"
    ))
    builder.add(types.InlineKeyboardButton(
        text="Я преподаватель",
        callback_data="teacher_authorization"
    ))

    await message.answer(START_MESSAGE, reply_markup=builder.as_markup())
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
    user_id = message.from_user.id
    note_name = get_last_note(user_id)
    note = FSInputFile(f"notes/{note_name}")

    await bot.send_message(chat_id=user_id, text="Твой последний конспект:")
    await bot.send_document(chat_id=user_id, document=note)
    await message.delete()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
