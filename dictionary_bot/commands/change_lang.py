from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from dictionary_bot.bot import Commands_of_words
from dictionary_bot.constans import START_SUPPORTED_LANGUAGES

from googletrans import Translator

from dictionary_bot.helpers import chunks
from dictionary_bot.models import Users

translator = Translator()


def change_lang(update: Update, context: CallbackContext):
    query = update.callback_query

    query.answer()

    user = Users.objects.get(
        chat_id=query.message.chat_id
    )

    langs_for_keyboard_filter_native = filter(
        lambda lang: lang["code"] != user.native_language,
        START_SUPPORTED_LANGUAGES
    )

    langs_for_keyboard_filter_target = filter(
        lambda lang: lang["code"] != user.target_language,
        langs_for_keyboard_filter_native
    )

    keyboard_buttons = list(map(lambda lang: InlineKeyboardButton(
        lang['name'],
        callback_data=f'{Commands_of_words.change_language.value}:{lang["code"]}'
    ), langs_for_keyboard_filter_target))

    keyboard_buttons = chunks(keyboard_buttons, 2)

    keyboard_buttons.append([InlineKeyboardButton('⬅️ Назад', callback_data=f'{Commands_of_words.to_back.value}')])

    keyboard = InlineKeyboardMarkup(keyboard_buttons)

    query.edit_message_text(
        text=query.message.text,
        reply_markup=keyboard
    )
