from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from dictionary_bot.bot import Commands_of_words
from dictionary_bot.commands import choose_target_lang
from dictionary_bot.models import Dictionary, Users
from dictionary_bot.utils import get_main_word_keyboard

from googletrans import Translator

translator = Translator()


def message_dict(update: Update, context: CallbackContext):

    user = Users.objects.get(
        chat_id=update.message.chat_id
    )

    word = update.message.text

    src_lang = translator.detect(word).lang
    dest_lang = user.target_language

    if src_lang == user.native_language:
        dest_lang = user.target_language
    elif user.native_language in src_lang:
        dest_lang = user.target_language
        src_lang = user.native_language
    else:
        dest_lang = user.native_language

    text_obj = translator.translate(word, src=src_lang, dest=dest_lang)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text_obj.text,
        reply_markup=get_main_word_keyboard(''),
        reply_to_message_id=update.message.message_id,
    )
