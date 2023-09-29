from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = '6437235439:AAF39_by7pIwn1-_oXwQnj8qH9hoE90cZec'
BOT_USERNAME: Final = '@ZadrugaS69_bot'

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE)
    await update.message.reply_text('UZMI GA ZDVIJE')