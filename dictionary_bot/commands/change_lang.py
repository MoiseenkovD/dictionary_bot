from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from dictionary_bot.bot import Commands_of_words
from dictionary_bot.constans import SUPPORTED_LANGUAGES

from googletrans import Translator

translator = Translator()


def change_lang(update: Update, context: CallbackContext):
    query = update.callback_query

    query.answer()

    original_word = query.message.reply_to_message.text
    translated_original_language = translator.detect(original_word).lang

    translated_word = query.message.text
    translated_language = translator.detect(translated_word).lang

    lang_buttons = []

    for lang in SUPPORTED_LANGUAGES:
        if translated_language == lang or translated_original_language == lang:
            continue
        lang_buttons.append([InlineKeyboardButton(lang, callback_data=f'{Commands_of_words.change_language.value}:{lang}')])

    lang_buttons.append([InlineKeyboardButton('⬅️ Назад', callback_data=f'{Commands_of_words.to_back.value}')])

    lang_keyboard = InlineKeyboardMarkup(lang_buttons)

    query.edit_message_text(
        text=query.message.text,
        reply_markup=lang_keyboard
    )