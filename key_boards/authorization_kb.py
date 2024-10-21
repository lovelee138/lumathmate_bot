from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_status():
    buttons = [
        [
            InlineKeyboardButton(text="Я ученик", callback_data="signup_student"),
            InlineKeyboardButton(text="Я преподаватель", callback_data="signup_teacher")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
