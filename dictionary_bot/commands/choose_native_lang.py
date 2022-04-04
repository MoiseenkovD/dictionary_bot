from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from dictionary_bot.bot import Commands_of_words
from dictionary_bot.helpers import chunks
from dictionary_bot.models import Users

from dictionary_bot.constans import START_SUPPORTED_LANGUAGES


def choose_native_lang(update: Update, context: CallbackContext):

    query = update.callback_query
    message = update.message or query.message

    user = Users.objects.get(
        chat_id=message.chat_id
    )

    if query is not None:
        query.answer()

        command, *payload = query.data.split(':')
        native_language = payload[0]

        user.native_language = native_language

        user.save()

    langs_for_keyboard = filter(lambda lang: lang["code"] != user.native_language, START_SUPPORTED_LANGUAGES)

    keyboard_buttons = list(map(lambda lang: InlineKeyboardButton(
        lang['name'],
        callback_data=f'{Commands_of_words.choose_target_lang.value}:{lang["code"]}'
    ), langs_for_keyboard))

    keyboard_buttons = chunks(keyboard_buttons, 2)

    keyboard = InlineKeyboardMarkup(keyboard_buttons)

    context.bot.send_message(
        chat_id=message.chat_id,
        text='Выберете язык который хотите изучать.',
        reply_markup=keyboard
    )
