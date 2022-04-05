from telegram import Update
from telegram.ext import CallbackContext

from dictionary_bot.models import Users

import dictionary_bot.commands as commands


def change_native_and_target_language(update: Update, context: CallbackContext):

    user = Users.objects.get(
        chat_id=update.message.chat_id
    )

    user.native_language = None
    user.target_language = None

    user.save()

    commands.start(update, context)
