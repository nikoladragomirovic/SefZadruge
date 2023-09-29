import json
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = '6437235439:AAF39_by7pIwn1-_oXwQnj8qH9hoE90cZec'
BOT_USERNAME: Final = '@ZadrugaS69_bot'
DATA_PATH: Final = './data.json'

def fetch_data():
    global DATA
    try:
        with open(DATA_PATH, 'r') as json_file:
            data = json.load(json_file)
        DATA = data
        return None
    except FileNotFoundError:
        print(f"File not found: {DATA_PATH}")
        return None
    except json.JSONDecodeError:
        print(f"Invalid JSON in file: {DATA_PATH}")
        return None

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('UZMI GA ZDVIJE')

def add_response(update: Update, context: ContextTypes.DEFAULT_TYPE):

    trigger, message = update.message.text.lstrip('/add ').split(';')

    new_response = {
        'trigger': trigger.lower(),
        'message': message
    }

    with open(DATA_PATH, 'r') as json_file:
        existing_data = json.load(json_file)

    existing_data.append(new_response)

    with open(DATA_PATH, 'w') as json_file:
        json.dump(existing_data, json_file, indent=3)

    fetch_data(); 

def remove_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    trigger_to_remove = update.message.text.lstrip('/remove ')
    
    with open(DATA_PATH, 'r') as json_file:
        existing_data = json.load(json_file)

    updated_data = [item for item in existing_data if item.get('trigger', '').lower() != trigger_to_remove.lower()]

    with open(DATA_PATH, 'w') as json_file:
        json.dump(updated_data, json_file, indent=3)

    fetch_data()
    # await update.message.reply_text(f'Response for trigger "{trigger_to_remove}" removed successfully.')


# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    data = DATA
    response_list = []

    for item in data:
        for key, value in item.items():
            if key == 'trigger' and value in processed:
                    response_list.append(item['message'])
    
    return response_list
    
async def handle_message(update: Update,context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str =update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    responses = handle_response(text)

    for response in responses:
        await update.message.reply_text(response)

async def error(update: Update,context: ContextTypes.DEFAULT_TYPE):
    pass

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Fetch Data
    fetch_data();

    # Commands
    app.add_handler(CommandHandler('start', start_command))

    app.add_handler(CommandHandler('add', add_response))
    app.add_handler(CommandHandler('remove', remove_response))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls
    print('Polling...')
    app.run_polling(poll_interval=3)