from telegram import Update

from telegram.ext import CallbackContext


def remove_translation(update: Update, context: CallbackContext):
    query = update.callback_query

    query.answer()

    query.message.reply_to_message.delete()
    query.message.delete()
