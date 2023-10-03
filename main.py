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
    except FileNotFoundError:
        print(f"File not found: {DATA_PATH}")
    except json.JSONDecodeError:
        print(f"Invalid JSON in file: {DATA_PATH}")

def add_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    trigger, message = update.message.text.lstrip('/add ').split(';')

    new_response = {
        'type': 'text',
        'trigger': trigger.lower(),
        'response': message
    }

    with open(DATA_PATH, 'r') as json_file:
        existing_data = json.load(json_file)

    existing_data.append(new_response)

    with open(DATA_PATH, 'w') as json_file:
        json.dump(existing_data, json_file, indent=3)

    fetch_data()

def remove_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    trigger_to_remove = update.message.text.lstrip('/remove ')
    
    with open(DATA_PATH, 'r') as json_file:
        existing_data = json.load(json_file)

    updated_data = [item for item in existing_data if item.get('trigger', '').lower() != trigger_to_remove.lower()]

    with open(DATA_PATH, 'w') as json_file:
        json.dump(updated_data, json_file, indent=3)

    fetch_data()

async def add_multimedia_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.caption[:5] == '/add ':

        trigger = update.message.caption[5:]

        if update.message.photo:
            file = await context.bot.get_file(update.message.photo[-1].file_id)
            await file.download_to_drive(f'./media/{file.file_unique_id}.jpg')
            response = f'./media/{file.file_unique_id}.jpg'
            type = 'image'

        if update.message.video:
            file = await context.bot.get_file(update.message.video.file_id)
            await file.download_to_drive(f'./media/{file.file_unique_id}.mp4')
            response = f'./media/{file.file_unique_id}.mp4'
            type = 'video'

        new_response = {
            'type': type,
            'trigger': trigger.lower(),
            'response': response
        }

        with open(DATA_PATH, 'r') as json_file:
            existing_data = json.load(json_file)

        existing_data.append(new_response)

        with open(DATA_PATH, 'w') as json_file:
            json.dump(existing_data, json_file, indent=2)

        fetch_data()

# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    response_list = []

    for item in DATA:
        for key, value in item.items():
            if key == 'trigger' and value in processed:
                    response_list.append((item['type'], item['response']))
    
    return response_list
    
async def handle_message(update: Update,context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str =update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    responses = handle_response(text)

    for response in responses:
        if response[0] == 'text':
            await update.message.reply_text(response[1])
        elif response[0] == 'image':
            await update.message.reply_photo(response[1])
        elif response[0] == 'video':
            await update.message.reply_video(response[1])

async def error(update: Update,context: ContextTypes.DEFAULT_TYPE):
    pass

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Fetch Data
    fetch_data();

    # Commands
    app.add_handler(CommandHandler('add', add_response))
    app.add_handler(CommandHandler('remove', remove_response))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT,handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, add_multimedia_response))
    app.add_handler(MessageHandler(filters.VIDEO, add_multimedia_response))

    # Errors
    app.add_error_handler(error)

    # Polls
    print('Polling...')
    app.run_polling(poll_interval=3)