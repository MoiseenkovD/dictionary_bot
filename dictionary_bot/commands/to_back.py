from telegram import Update
from telegram.ext import CallbackContext

from googletrans import Translator

from dictionary_bot.models import Users
from dictionary_bot.utils import get_main_word_keyboard

translator = Translator()


def to_back(update: Update, context: CallbackContext):
    query = update.callback_query

    query.answer()

    command, *payload = query.data.split(':')

    user = Users.objects.get(
        chat_id=query.message.chat_id
    )

    word = query.message.reply_to_message.text

    lang_code = translator.detect(word).lang

    # dest = 'ru'
    #
    # if 'ru' in lang:
    #     dest = 'en'
    # else:
    #     dest = 'ru'
    #

    # if lang_code == user.native_language:
    #     lang_code = user.target_language
    # else:
    #     lang_code = user.native_language
    #
    # translated_word = translator.translate(word, dest=lang_code).text

    if lang_code == user.native_language:
        dest_lang = user.target_language
    elif user.native_language in lang_code:
        dest_lang = user.target_language
        lang_code = user.native_language
    else:
        dest_lang = user.native_language

    translated_word = translator.translate(word, src=lang_code, dest=dest_lang).text

    query.edit_message_text(
        text=translated_word,
        reply_markup=get_main_word_keyboard('')
    )