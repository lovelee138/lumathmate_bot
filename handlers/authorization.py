from aiogram import Bot, Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import db.get as get
import db.check as check
import db.add as add
from key_boards import authorization_kb


router = Router()


class Authorization(StatesGroup):
    choosing_status = State()
    inputing_member_id = State()
    inputing_name = State()


@router.message(StateFilter(None), Command("start"))
async def cmd_start(message: types.message, state: FSMContext, bot: Bot):
    user_tg_id = message.from_user.id
    authorizied_user_id = check.signed_up(user_tg_id)

    if authorizied_user_id:
        authorizied_user_name = get.name_by_id(authorizied_user_id)
        await message.answer(
            f"Добро пожаловать, {authorizied_user_name}!\nНажмите /help, чтобы посмотреть доступные команды.",
        )
    else:
        kb_status = authorization_kb.get_keyboard_status()
        await bot.answer(
            "Вы пока не зарегистрированы! Давайте исправим это! Для этого нужно будет ответить на пару вопросов  :D",
            reply_markup=kb_status,
        )

        await state.set_state(Authorization.choosing_status)

    await state.set_data(
        {"tg_id": None, "member_id": None, "status": None, "name": None}
    )


@router.callback_query(F.data.startswith("signup_"), Authorization.choosing_status)
async def sign_up(callback: types.CallbackQuery, state: FSMContext):
    status = callback.data.split("_")[1]

    if status == "teacher":
        await callback.message.answer(
            "Я буду рад помочь Вам в преподавании! Давайте знакомиться. Меня зовут lu_mathmate_bot.\
            друзей просто lu. Как я могу Вас называть?"
        )

        new_member_id = get.new_member_id("teacher")
        await state.update_data(status="teacher", member_id=new_member_id)
        await state.set_state(Authorization.inputing_name)
    elif status == "student":
        await callback.message.answer(
            "Я буду рад помочь Вам в обучении. Но сначала мне нужно найти Вас и Вашего учителя. \
            Пожалуйста, введите идентификатор, выданный преподавателем:"
        )

        await state.update_data(status="student")
        await state.set_state(Authorization.inputing_member_id)


@router.message(Authorization.inputing_member_id, F.text)
async def check_new_student(message: types.message, bot: Bot, state: FSMContext):
    user_tg_id = message.from_user.id
    member_id = int(message.text)

    if check.stud_member_id_correct(member_id):
        await message.answer(
            "Отлично! Я Вас нашёл! Самое время познакомиться. Меня зовут lu_mathmate_bot. Для друзей просто lu. Как я могу к Вам обращаться?",
        )

        await state.update_data(member_id=member_id)
        await state.set_state(Authorization.inputing_name)
    else:
        await message.answer(
            "К сожалению, у меня не получается найти Вас. проверьте, пожалуйста, идентификатор.",
        )


@router.message(Authorization.inputing_name, F.text)
async def set_name(message: types.message, bot: Bot, state: FSMContext):
    await state.update_data(name=message.text, tg_id=message.from_user.id)

    user_data = await state.get_data()
    add.new_member(
        user_data["tg_id"],
        user_data["member_id"],
        user_data["name"],
        user_data["status"],
    )

    await message.answer(
        "Авторизация прошла успешно!\nНажмите /help, чтобы открыть список доступных команд.",
    )
    await state.clear()
