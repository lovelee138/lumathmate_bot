from aiogram import Bot, Router, types, F
from aiogram.types import FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
import aiogram
from key_boards import choice_kb
import db.get as get
import db.check as check


MAX_VISIBLE = 3


class ShowingNotes(StatesGroup):
    showing = State()


router = Router()


@router.message(Command("cancel"), StateFilter(ShowingNotes))
async def cancel(message: types.message, state: FSMContext):
    await message.answer("Упс! Вы отменили запрос на получение конспекта")
    await state.clear()


async def send_message_with_keyboard_choice(state: FSMContext, direction, message):
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
    await message.answer(
        f"Выберите конспект, который вы хотите получить:\n{descriptions}",
        reply_markup=kb,
    )

    await state.update_data({"last_displayed": end - 1})


@router.message(Command("get_note"))
async def get_note(message: types.message, state: FSMContext, bot: Bot):
    id_stud = get.member_id(message.from_user.id)
    status = get.status_by_id(id_stud)

    if status == "teacher":
        await message.answer(
            """Упс! Эта функция предназначена для учеников!
Нажмите /help, чтобы просмотреть возможные команды."""
        )
        return
    await state.set_state(ShowingNotes.showing)
    notes = get.list_of_notes(id_stud)
    await state.set_data(
        {
            "last_displayed": -1,
            "notes": notes,
        }
    )

    await send_message_with_keyboard_choice(state, 1, message)


@router.callback_query(F.data.startswith("choice_"), StateFilter(ShowingNotes))
async def answer_to_choice(callback: types.callback_query, state: FSMContext, bot: Bot):
    user = callback.from_user.id
    choice = callback.data.split("_")[1]
    if choice == "next":
        await send_message_with_keyboard_choice(state, 1, callback.message)
    elif choice == "previous":
        await send_message_with_keyboard_choice(state, -1, callback.message)
    elif choice.isdigit():
        user_data = await state.get_data()
        note = user_data["notes"][int(choice) - 1]
        try:
            file_id = note[4]
            await callback.message.answer_document(file_id)
        except Exception:
            document = FSInputFile(note[3] + note[0])
            await callback.message.answer_document(document)

        await state.clear()
    await callback.answer()


@router.callback_query(F.data.startswith("choice_"), StateFilter(None))
async def answer_to_incorrect_choice(callback: types.callback_query, bot: Bot):
    await callback.answer("Ошибка! Кнопка из старого запроса.")
    await callback.message.answer(
        "Нажмите /help, чтобы увидеть список доступных\
         функций.",
    )
