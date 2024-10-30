from aiogram import Bot, Dispatcher, Router, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from key_boards import choice_kb
from db_actions import *


class ShowingNotes(StatesGroup):
    showing = State()


router = Router()


@router.message(Command("get_note"))
async def get_note(message: types.message):
    student_id = get_member_id_by_tg_id(message.from_user.id)
    notes = get_list_of_notes(student_id)
    kb = choice_kb.get_keyboard_choice(min(len(notes), 3), True)
    await message.answer(
        f"{notes}\nВыберите конспект, который вы хотите получить:", reply_markup=kb
    )
