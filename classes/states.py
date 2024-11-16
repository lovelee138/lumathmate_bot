from aiogram.fsm.state import StatesGroup, State


class Authorization(StatesGroup):
    choosing_status = State()
    inputing_member_id = State()
    inputing_name = State()
    authorizied = State()


class SendingNote(StatesGroup):
    identification = State()
    getting_description = State()
    getting_number = State()
    getting_date = State()
    getting_file = State()
    confirmation = State()


class ShowingNotes(StatesGroup):
    showing = State()


class Status(StatesGroup):
    unknown = State()
    teacher = State()
    student = State()
