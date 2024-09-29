import json
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued"""
    user = update.effective_user
    await context.bot.send_message(user.id, "wooooo")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    with open('help_info.json', "r") as file:
        help_info = json.load(file)
    text = "Я дружелюбный боt :D\n\n"
    for key in help_info.keys():
        text += f"/{key} - {help_info[key]}\n"

    await context.bot.send_message(user.id, text)


def main():
    application = Application.builder().token("5591040510:AAGUOdFLHiog-FWDcO2m7l38ibpu8qNFE10").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
    