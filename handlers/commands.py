from aiogram import Bot, Router, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from .constants import *
import db.get as get


router = Router()

# Common


@router.message(Command("help"))
async def help_command(message: types.message):
    id_stud = get.member_id(message.from_user.id)
    status = get.status_by_id(id_stud)
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
@router.message(Command("show_all_students"))
async def send_all_students(message: types.message):
    print(message.from_user.id)
    member_id = get.member_id(message.from_user.id)
    status = get.status_by_id(member_id)
    if status == "student":
        await message.answer(
            "Упс! Эта функция не для вас! \
            Нажмите /help, чтобы получить список функций."
        )
    else:
        student_list = get.all_students(member_id)
        student_list_text = ""
        for id, name in student_list:
            student_list_text += "{} ({})\n".format(name, id)
        await message.answer(
            f"Список ваших студентов (в скобках указан id):\n{student_list_text}"
        )
