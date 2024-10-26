from aiogram import Bot, Router, types, F
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from db_actions import *
from key_boards import confirmation_kb


router = Router()


class SendingNote(StatesGroup):
    identification = State()
    getting_description = State()
    getting_number = State()
    getting_date = State()
    getting_file = State()
    confirmation = State()


async def confirmation(message: types.message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer("Подтвердите данные о конспекте:")
    student_name = get_student_name(user_data["student_id"])
    text = f"""
Имя ученика: {student_name}
Описание конспекта: {user_data["description"]}
Дата конспекта: {user_data["date"]}
Номер конспекта: {user_data["number"]}
    """
    kb = confirmation_kb.get_keyboard_confirm()
    await message.answer(text, reply_markup=kb)
    await state.set_state(SendingNote.confirmation)


@router.message(StateFilter(None), Command("send_note"))
async def send_note(message: types.message, state: FSMContext, command: CommandObject):
    tg_id = message.from_user.id
    status = get_status_by_id(tg_id)
    if status == "teacher":
        await message.answer("Ура! Еще один файл со знаниями будет загружен!")
        await state.set_state(SendingNote.getting_description)
    elif status == "student":
        await message.answer("Загружать конспекты могут только преподаватели :(")
    else:
        await message.answer("Ошибка, вы кто? Пройдите регистрацию /start")

    await state.set_data({"student_id": None, "description": None, "number": None, "date": None, "file": None})

    if not (command.args is None):
        student_id = is_student_name_correct(command.args, tg_id)
        if student_id:
            await state.update_data(student_id=student_id)
            await message.answer('Напишите описание этого конспекта. Если описание не нужно, введите "далее"')
            await state.set_state(SendingNote.getting_description)
        else:
            await message.answer("Введите имя ученика, которому вы хотите отправить конспект. Чтобы посмотреть список всех учеников нажмите /show_all_students")
            await state.set_state(SendingNote.identification)
    else:
        await message.answer("Введите имя ученика, которому вы хотите отправить конспект. Чтобы посмотреть список всех учеников нажмите /show_all_students")
        await state.set_state(SendingNote.identification)


@router.message(StateFilter(SendingNote), Command("cancel"))
async def cancsel(message: types.message, state: FSMContext):
    await message.answer("Упс! Вы отменили отправку конспекта")
    await state.clear()


@router.message(
    SendingNote.identification
)
async def student_name(message: types.message, state: FSMContext):
    tg_id = message.from_user.id
    student_id = is_student_name_correct(message.text, tg_id)
    if student_id:
        await state.update_data(student_id=student_id)
        await message.answer('Напишите описание этого конспекта. Если описание не нужно, введите "далее"')
        user_data = await state.get_data()
        if user_data["description"] is None:
            await state.set_state(SendingNote.getting_description)
        else:
            await confirmation(message, state)
    else:
        await message.answer("Такого ученика нет, попробуйте еще раз:")
        await state.set_state(SendingNote.identification)
    

@router.message(
    SendingNote.getting_description
)
async def description(message: types.message, state: FSMContext):
    description = message.text
    
    if description.lower() == "далее":
        await state.update_data(description="")
    else:
        await state.update_data(description=description)

    date=message.date.date()
    await state.update_data(date=date)

    user_data = await state.get_data()
    
    number = get_last_note_number(user_data["student_id"])
    await state.update_data(number=number+1)

    await confirmation(message, state)


@router.message(
    F.document,
    SendingNote.getting_file
)
async def get_file(message: types.message, state: FSMContext):
    user_data = await state.get_data()
    print(user_data)


@router.callback_query(
    F.data == "confirmed",
    SendingNote.confirmation
)
async def data_confirmed(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    await bot.send_message(callback.from_user.id, "Отлично! Теперь отправьте pdf-файл с конспектом")
    await state.set_state(SendingNote.getting_file)
    await callback.answer()


@router.callback_query(
    F.data == "non_confirmed",
    SendingNote.confirmation
)
async def data_confirmed(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    kb = confirmation_kb.get_keyboard_edit_choice()
    await bot.send_message(callback.from_user.id, "Что бы вы хотели исправить?", reply_markup=kb)
    await callback.answer()



@router.message(
    SendingNote.getting_date
)
async def get_date(message: types.message, state: FSMContext):
    try:
        year, month, day = message.text.split("-")
        int(year)
        int(month)
        int(day)
        await state.update_data(date=message.text)
        await confirmation(message, state)
    except Exception:
        await message.answer("Неверный формат! Попробуйте еще раз.\nПример: 2024-01-31")        


@router.message(
    SendingNote.getting_number
)
async def get_number(message: types.message, state: FSMContext):
    try:
        n = int(message.text)
        user_data = await state.get_data()
        student_id = user_data["student_id"]
        if not is_note_number_correct(student_id, n):
            await state.update_data(number=n)
            await confirmation(message, state)
        else:
            await message.answer("Такой номер конспекта уже есть! Попробуйте еще раз.")
    except ValueError:
        await message.answer("Неверный формат! Введите целое число!")


@router.callback_query(
    F.data.startswith("edit_")
)
async def edit(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    user_id = callback.from_user.id
    choice = callback.data.split("_")[1]

    if choice == "name":
        await bot.send_message(user_id, "Введите имя ученика, которому вы хотите отправить конспект. Чтобы посмотреть список всех учеников нажмите /show_all_students")
        await state.set_state(SendingNote.identification)
    elif choice == "description":
        await bot.send_message(user_id, 'Напишите описание этого конспекта. Если описание не нужно, введите "далее"')
        await state.set_state(SendingNote.getting_description)
    elif choice == "date":
        await bot.send_message(user_id, "Введите дату в формате yyyy-mm-dd. Например, 2024-01-31")
        await state.set_state(SendingNote.getting_date)
    elif choice == "number":
        await bot.send_message(user_id, "Введите целое число - номер конспекта")
        await state.set_state(SendingNote.getting_number)  
    await callback.answer()