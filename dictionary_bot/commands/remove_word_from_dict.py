from telegram import Update

from telegram.ext import CallbackContext

from dictionary_bot.models import Dictionary


def remove_word_from_dict(update: Update, context: CallbackContext):
    query = update.callback_query

    query.answer()

    command, *payload = query.data.split(':')

    word_id = payload[0]

    Dictionary.objects.filter(id=word_id).delete()

    query.edit_message_text(
        text='✅ Перевод успешно удален'
    )
