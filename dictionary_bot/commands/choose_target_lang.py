from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

import dictionary_bot.bot
from dictionary_bot.models import Users


def choose_target_lang(update: Update, context: CallbackContext):
    query = update.callback_query

    query.answer()

    command, *payload = query.data.split(':')

    user = Users.objects.get(
        chat_id=query.message.chat_id
    )

    target_language = payload[0]

    user.target_language = target_language

    user.save()

    context.bot.send_message(
        chat_id=query.message.chat_id,
        text='Отлично, вы готовы приступить к изучению нового языка!\n'
             'Напишите мне слово '
    )


