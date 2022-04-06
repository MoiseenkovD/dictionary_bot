from telegram import Update
from telegram.ext import CallbackContext

from googletrans import Translator

from dictionary_bot.models import Users
from dictionary_bot.utils import get_main_word_keyboard

translator = Translator()


def change_translation_word(update: Update, context: CallbackContext, payload):

    query = update.callback_query

    query.answer()

    command, *payload = query.data.split(':')

    user = Users.objects.get(
        chat_id=query.message.chat_id
    )

    original_word = query.message.reply_to_message.text

    lang_code = translator.detect(original_word).lang

    # if lang_code == 'en':
    #     lang_code = 'ru'
    # else:
    #     lang_code = 'en'

    # if lang_code == user.native_language:
    #     lang_code = user.target_language
    # else:
    #     lang_code = user.native_language

    dest_lang = user.target_language

    if lang_code == user.native_language:
        dest_lang = user.target_language
    elif user.native_language in lang_code:
        dest_lang = user.target_language
        lang_code = user.native_language
    else:
        dest_lang = user.native_language

    translated_word = translator.translate(original_word, src=lang_code, dest=dest_lang).extra_data['all-translations']

    type_of_word = int(payload[0])

    index_of_word = int(payload[1])

    query.edit_message_text(
        text=translated_word[type_of_word][1][index_of_word],
        reply_markup=get_main_word_keyboard('')
    )