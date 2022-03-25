from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext

from dictionary_bot.bot import Commands_of_words
from dictionary_bot.constans import SUPPORTED_LANGUAGES

from googletrans import Translator

from dictionary_bot.helpers import chunks

translator = Translator()


def check_translation_type(update: Update, context: CallbackContext, payload):

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

    word_type_index = int(payload[0])

    buttons = []

    for i, word in enumerate(translated_word[word_type_index][1]):
        buttons.append(
            InlineKeyboardButton(
                word.title(),
                callback_data=f'{Commands_of_words.change_translation_word.value}:{word_type_index}:{i}'
            )
        )

    buttons = chunks(buttons, 2)

    buttons.append([InlineKeyboardButton('⬅️ Назад', callback_data=f'{Commands_of_words.to_back.value}')])

    keyboard_words = InlineKeyboardMarkup(buttons)

    query.edit_message_text(
        text=query.message.text,
        reply_markup=keyboard_words,
    )