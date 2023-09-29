from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = '6437235439:AAF39_by7pIwn1-_oXwQnj8qH9hoE90cZec'
BOT_USERNAME: Final = '@ZadrugaS69_bot'

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('UZMI GA ZDVIJE')

# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'matrix' in processed:
        return 'DUVAJ GA MAHIME'
    if 'matriks' in processed:
        return 'DUVAJ GA MAHIME'
    
async def handle_message(update: Update,context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str =update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    response : str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update,context: ContextTypes.DEFAULT_TYPE):
    pass

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls
    print('Polling...')
    app.run_polling(poll_interval=3)