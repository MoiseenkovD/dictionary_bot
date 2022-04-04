from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from dictionary_bot.bot import Commands_of_words
from dictionary_bot.helpers import chunks
from dictionary_bot.models import Users

from dictionary_bot.constans import START_SUPPORTED_LANGUAGES


def start(update: Update, context: CallbackContext):
    user = Users.objects.get_or_create(
        chat_id=update.message.chat_id,
    )[0]

    user.first_name = update.message.chat.first_name
    user.last_name = update.message.chat.last_name
    user.username = update.message.chat.username

    user.save()

    if user.native_language is None:
        keyboard_buttons = list(map(lambda lang: InlineKeyboardButton(
            lang['name'],
            callback_data=f'{Commands_of_words.choose_native_lang.value}:{lang["code"]}'
        ), START_SUPPORTED_LANGUAGES))

        keyboard_buttons = chunks(keyboard_buttons, 2)

        keyboard = InlineKeyboardMarkup(keyboard_buttons)

        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Привет. \n"
                 "Выбери свой родной язык !",
            reply_markup=keyboard
        )
    else:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Напишите мне слово для перевода",
        )
