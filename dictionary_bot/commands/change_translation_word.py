from telegram import Update
from telegram.ext import CallbackContext

from googletrans import Translator

from dictionary_bot.utils import get_main_word_keyboard

translator = Translator()


def change_translation_word(update: Update, context: CallbackContext, payload):

    query = update.callback_query

    query.answer()

    command, *payload = query.data.split(':')

    original_word = query.message.reply_to_message.text

    lang_code = translator.detect(original_word).lang

    if lang_code == 'en':
        lang_code = 'ru'
    else:
        lang_code = 'en'

    translated_word = translator.translate(original_word, dest=lang_code).extra_data['all-translations']

    type_of_word = int(payload[0])

    index_of_word = int(payload[1])

    query.edit_message_text(
        text=translated_word[type_of_word][1][index_of_word],
        reply_markup=get_main_word_keyboard('')
    )