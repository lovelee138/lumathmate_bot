from aiogram import Bot, Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode
from db_actions import *
from .constants import *


router = Router()

# Common

@router.message(Command("help"))
async def help_command(message: types.message):
    status = get_status_by_id(message.from_user.id)
    if status == "teacher":
        await message.answer(HELP_COMMAND_TEACHER, parse_mode=ParseMode.HTML)
    elif status == "student":
        await message.answer(HELP_COMMAND_STUDENT, parse_mode=ParseMode.HTML)
    else:
        await message.answer("Ошибка! Нажмите /start, чтобы авторизоваться")

    await message.delete()


@router.message(Command("info"))
async def help_command(message: types.message):
    await message.answer(INFO_MESSAGE)
    await message.delete()


# For teachers


# For students

@router.message(Command("get_note"))
async def help_command(message: types.message, bot: Bot):
    user_id = message.from_user.id
    note_name = get_last_note(user_id)
    note = FSInputFile(f"notes/{note_name}")

    await bot.send_message(chat_id=user_id, text="Твой последний конспект:")
    await bot.send_document(chat_id=user_id, document=note)
    await message.delete()
