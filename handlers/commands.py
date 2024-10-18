from aiogram import Bot, Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from db_actions import *
from .constants import *


router = Router()


@router.message(Command("help"))
async def help_command(message: types.message):
    await message.answer(HELP_COMMAND)
    await message.delete()


@router.message(Command("info"))
async def help_command(message: types.message):
    await message.answer(INFO_MESSAGE)
    await message.delete()


@router.message(Command("get_note"))
async def help_command(message: types.message, bot: Bot):
    user_id = message.from_user.id
    note_name = get_last_note(user_id)
    note = FSInputFile(f"notes/{note_name}")

    await bot.send_message(chat_id=user_id, text="Твой последний конспект:")
    await bot.send_document(chat_id=user_id, document=note)
    await message.delete()
