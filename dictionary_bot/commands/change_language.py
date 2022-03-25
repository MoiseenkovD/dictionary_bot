from telegram import Update
from telegram.ext import CallbackContext

from googletrans import Translator

from dictionary_bot.utils import get_main_word_keyboard

translator = Translator()


def change_language(update: Update, context: CallbackContext, payload):
    query = update.callback_query

    query.answer()

    command, *payload = query.data.split(':')

    word = query.message.text

    lang = translator.detect(word).lang

    translated_word = translator.translate(word, dest=payload[0]).text

    query.edit_message_text(
        text=translated_word,
        reply_markup=get_main_word_keyboard('')
    )
