from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_choice(n: int, next=False):
    buttons = [
        [InlineKeyboardButton(text=f"{i}", callback_data=f"choice_{i}") for i in range(1, n+1)]
    ]
    if next:
        buttons.append([InlineKeyboardButton(text="Далее", callback_data="choice_next")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
