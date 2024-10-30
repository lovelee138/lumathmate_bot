from aiogram import Bot, Router, types, F
from aiogram.types import FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
import aiogram
from key_boards import choice_kb
from db_actions import *


MAX_VISIBLE = 3


class ShowingNotes(StatesGroup):
    showing = State()


router = Router()


@router.message(Command("cancel"), StateFilter(ShowingNotes))
async def cancel(message: types.message, state: FSMContext):
    await message.answer("Упс! Вы отменили запрос на получение конспекта")
    await state.clear()


async def send_message_with_keyboard_choice(state: FSMContext, direction, to_id, bot):
    descriptions = ""
    displayed_data = await state.get_data()
    notes = displayed_data["notes"]

    if direction == 1:
        start = displayed_data["last_displayed"] + 1
        end = min(start + MAX_VISIBLE, len(notes))
    else:
        end = displayed_data["last_displayed"]
        start = max(end - MAX_VISIBLE, 0)

    for i in range(start, end):
        descriptions += f"{i+1}. "
        descr_path = notes[i][3] + notes[i][0] + "_description.txt"
        with open(descr_path, "r") as file:
            descriptions += file.read()
        descriptions += "\n"

    next = end < len(notes)
    previous = start > 0

    kb = choice_kb.get_keyboard_choice(start + 1, end + 1, next, previous)
    await bot.send_message(
        to_id,
        f"Выберите конспект, который вы хотите получить:\n{descriptions}",
        reply_markup=kb,
    )

    await state.update_data({"last_displayed": end - 1})


@router.message(Command("get_note"))
async def get_note(message: types.message, state: FSMContext, bot: Bot):
    student_id = get_member_id_by_tg_id(message.from_user.id)
    status = get_status_by_id(message.from_user.id)

    if status == "teacher":
        await message.answer(
            """Упс! Эта функция предназначена для учеников!
Нажмите /help, чтобы просмотреть возможные команды."""
        )
        return
    await state.set_state(ShowingNotes.showing)
    notes = get_list_of_notes(student_id)
    await state.set_data(
        {
            "last_displayed": -1,
            "notes": notes,
        }
    )

    await send_message_with_keyboard_choice(state, 1, message.from_user.id, bot)


@router.callback_query(F.data.startswith("choice_"), StateFilter(ShowingNotes))
async def answer_to_choice(callback: types.callback_query, state: FSMContext, bot: Bot):
    user = callback.from_user.id
    choice = callback.data.split("_")[1]
    if choice == "next":
        await send_message_with_keyboard_choice(state, 1, user, bot)
    elif choice == "previous":
        await send_message_with_keyboard_choice(state, -1, user, bot)
    elif choice.isdigit():
        user_data = await state.get_data()
        note = user_data["notes"][int(choice) - 1]
        try:
            file_id = note[4]
            await bot.send_document(user, file_id)
        except Exception:
            document = FSInputFile(note[3] + note[0])
            await bot.send_document(user, document)

        await state.clear()
    await callback.answer()


@router.callback_query(F.data.startswith("choice_"), StateFilter(None))
async def answer_to_incorrect_choice(callback: types.callback_query, bot: Bot):
    await callback.answer("Ошибка! Кнопка из старого запроса.")
    await bot.send_message(
        callback.from_user.id,
        "Нажмите /help, чтобы увидеть список доступных\
                           функций.",
    )
