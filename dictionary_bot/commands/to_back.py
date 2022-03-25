from telegram import Update
from telegram.ext import CallbackContext

from googletrans import Translator

from dictionary_bot.utils import get_main_word_keyboard

translator = Translator()


def to_back(update: Update, context: CallbackContext):
    query = update.callback_query

    query.answer()

    command, *payload = query.data.split(':')

    word = query.message.reply_to_message.text

    lang = translator.detect(word).lang

    dest = 'ru'

    if 'ru' in lang:
        dest = 'en'
    else:
        dest = 'ru'

    translated_word = translator.translate(word, dest=dest).text

    query.edit_message_text(
        text=translated_word,
        reply_markup=get_main_word_keyboard('')
    )