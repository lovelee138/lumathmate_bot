import json
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from db_actions import *


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued"""
    user = update.effective_user
    print(user.username)
    await context.bot.send_message(user.id, "wooooo")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    with open('help_info.json', "r") as file:
        help_info = json.load(file)
    text = "Я дружелюбный боt   :D\n\n"
    for key in help_info.keys():
        text += f"/{key} - {help_info[key]}\n"

    await context.bot.send_message(user.id, text)


async def get_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    note_name = get_last_note(user.id)
    await context.bot.send_document(user.id, f"notes/{note_name}")


async def load_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await context.bot.send_message(user.id, "Input student's username:\n(/show_students to see student's list)")


async def show_students(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    all_students = get_students(user.username)
    
    msg_all_students = "Your students:\n"
    for student in all_students:
        msg_all_students += f"@{student}\n"
    await context.bot.send_message(user.id, msg_all_students)


def add_all_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("get_note", get_note))
    application.add_handler(CommandHandler("load_note", load_note))
    application.add_handler(CommandHandler("show_students", show_students))


def main():
    config = load_config(filename="config/bot.ini", section="bot")
    application = Application.builder().token(config["token"]).build()
    add_all_handlers(application)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

