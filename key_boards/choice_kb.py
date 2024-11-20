from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_choice(start: int, end: int, next=False, previous=False):
    buttons = [
        [
            InlineKeyboardButton(text=f"{i}", callback_data=f"choice_{i}")
            for i in range(start, end + 1)
        ]
    ]
    if next:
        buttons.append(
            [InlineKeyboardButton(text="Далее", callback_data="choice_next")]
        )
    if previous:
        buttons.append(
            [InlineKeyboardButton(text="Предыдущая", callback_data="choice_previous")]
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
