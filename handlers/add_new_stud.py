from aiogram import types, Router, F, Bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from db import get, add
from key_boards import get_keyboard_confirm


router = Router()

class NewStudent(StatesGroup):
    name = State()
    checking = State()


@router.message(StateFilter(NewStudent), Command("cancel"))
async def cancel(message: types.message, state: FSMContext):
    await message.answer("Вы отменили добавление нового ученика. Нажмите /help, чтобы посмотреть список доступных команд.")
    await state.clear()


@router.message(Command("add_new_student"))
async def add_new_student_start(message: types.message, state: FSMContext):
    id_teac = get.member_id(message.from_user.id)

    await state.set_data({"id_teac": id_teac, "name_stud": None, "id_stud": None})
    await message.answer("Давайте добавим нового ученика! Введите его имя:")
    await state.set_state(NewStudent.name)


@router.message(NewStudent.name)
async def check_data(message: types.message, state: FSMContext):
    await state.update_data(name=message.text)
    
    confirm_kb = get_keyboard_confirm()
    await message.answer(text=f"Вы хотите добавить ученика по имени {message.text}, верно?", reply_markup=confirm_kb)
    await state.set_state(NewStudent.checking)


@router.callback_query(F.data=="confirmed", NewStudent.checking)
async def give_member_id(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    tg_id = callback.from_user.id

    new_member_id = get.new_member_id("student")

    await bot.send_message(text=f"Отлично! Я зарегистрировал для Вас нового ученика. Вот его id участника: {new_member_id}. При первой авторизации ему потребуется этот id.", chat_id=tg_id)

    await state.update_data(id_stud=new_member_id)
    
    info = await state.get_data()
    add.new_student(info["id_stud"], info["id_teac"], info["name"])

    await state.clear()
    await callback.answer()


@router.callback_query(F.data=="non_confirmed", NewStudent.checking)
async def get_name_again(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    tg_id = callback.from_user.id

    await bot.send_message(text=f"Если хотите отменить добавление нового ученика, нажмите /cancel. Если хотите изменить имя, введите новое.", chat_id=tg_id)

    await state.set_state(NewStudent.name)
    await callback.answer()
    
