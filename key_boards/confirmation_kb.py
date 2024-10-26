from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_confirm():
    buttons = [
        [
            InlineKeyboardButton(text="Все верно!", callback_data="confirmed"),
            InlineKeyboardButton(text="Неверно :(", callback_data="non_confirmed")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_keyboard_edit_choice():
    buttons = [
        [
            InlineKeyboardButton(text="Имя", callback_data="edit_name"),
            InlineKeyboardButton(text="Описание", callback_data="edit_description"),
            InlineKeyboardButton(text="Дату", callback_data="edit_date"),
            InlineKeyboardButton(text="Номер", callback_data="edit_number")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard