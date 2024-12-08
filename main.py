import os
from typing import Final
from dotenv import load_dotenv, find_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext

from bot_engine.Images import Images
from bot_engine.Chat import Chat

# Constants
load_dotenv(find_dotenv(), override=True)
TOKEN: Final[str] = os.getenv('TOKEN')
BOT_USERNAME: Final[str] = os.getenv('BOT_USERNAME')
chat: Chat = Chat()
images: Images = Images()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello there, nice to meet you! Let\'s chat!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Just type something and I will respond to you!')

async def role_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text: str = update.message.text.replace(f'/role', '').strip()
    text: str = text.replace(f'{BOT_USERNAME}', '').strip()
    user: str = update.message.from_user.username
    print(text, user)
    if len(text) > 0:
        chat.chat.custom_role[user] = text
    await update.message.reply_text(f'Це моя роль для {user} "{chat.chat.get_custom_role(user)}"')

def handle_response(user: str, text: str) -> str:
    processed: str = text.lower()[:1000]

    chat.set_request(processed, user)
    return chat.get_response(user)

    # if 'hello' in processed:
    #     return 'Hey there'
    #
    # if 'how are you' in processed:
    #     return 'I\'m god, thank you!'
    #
    # if 'i love python' in processed:
    #     return 'Python loves you too!'
    #
    # return 'I do not understand you!'

async def handle_draw(text: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if 'намалюй' in text:
        images.set_request(text)
        filename = images.get_response()
        print(filename)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(filename, 'rb'))
        return True

    return False


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_type: str = update.message.chat.type
    text: str = update.message.text
    user: str = update.message.from_user.username

    # Log
    print(f'User {user} in {message_type}: {text}')

    # Handle message type
    if message_type == 'group' or message_type == 'supergroup':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            res = await handle_draw(new_text, update, context)
            if res:
                return
            response = handle_response(user, new_text)
        else:
            return
    else:
        res = await handle_draw(text, update, context)
        if res:
            return
        response: str = handle_response(user, text)

    print(f'Bot response: {response}')
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f'Update {update} caused error {context.error}')

def main():
    print('Starting telegram bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('role', role_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=5)

if __name__ == '__main__':
    main()
