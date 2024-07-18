# telegrambot/telegram_bot.py
import os
import sys
import django
import requests
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Quickaid.settings')
django.setup()

# from users.models import EmergencyContact

# bot_token = '7434036135:AAFap6m_cje5igj5gvj4NUMGcxuxlx7PYEM'
# url = f"https://api.telegram.org/bot{bot_token}/"


from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Send /getid to get your chat ID.')

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    await update.message.reply_text(f'Your chat ID is: {chat_id}')

def main() -> None:
    app = ApplicationBuilder().token('7434036135:AAFap6m_cje5igj5gvj4NUMGcxuxlx7PYEM').build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("getid", get_id))

    app.run_polling()

if __name__ == '__main__':
    main()

