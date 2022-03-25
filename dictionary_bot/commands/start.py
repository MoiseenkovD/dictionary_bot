from telegram import Update
from telegram.ext import CallbackContext

from dictionary_bot.models import Users

def start(update: Update, context: CallbackContext):
    user = Users.objects.get_or_create(
        chat_id=update.message.chat_id,
    )[0]

    user.first_name = update.message.chat.first_name
    user.last_name = update.message.chat.last_name
    user.username = update.message.chat.username

    user.save()

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Напишите слово для перевода"
    )