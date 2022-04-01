from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from dictionary_bot.bot import Commands_of_words
from dictionary_bot.models import Dictionary, Users
from dictionary_bot.utils import get_main_word_keyboard

from googletrans import Translator

translator = Translator()


def message_dict(update: Update, context: CallbackContext):
    word = update.message.text

    lang = translator.detect(word).lang

    dest = 'ru'

    if 'ru' in lang:
        dest = 'en'
    else:
        dest = 'ru'

    text_obj = translator.translate(word, dest=dest)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text_obj.text,
        reply_markup=get_main_word_keyboard(''),
        reply_to_message_id=update.message.message_id,
    )
