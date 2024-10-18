import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from handlers import commands
from db_actions import *

START_MESSAGE = """
Привет! Я твой помощник в изучении математики!
Сначала тебе нужно зарегистрироваться в сервисе.
"""

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


async def main():
    BOT_TOKEN = load_config(filename="config/bot.ini", section="bot")["token"]
    bot = Bot(BOT_TOKEN)

    dp.include_routers(commands.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())
