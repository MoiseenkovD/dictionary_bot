from telegram import Update

from telegram.ext import CallbackContext

from dictionary_bot.models import Users, Dictionary


def update_meaning(update: Update, context: CallbackContext):
    query = update.callback_query

    query.answer()

    command, *payload = query.data.split(':')
    word_id = payload[0]

    user = Users.objects.get(
        chat_id=query.message.chat_id
    )

    word = Dictionary.objects.filter(
        user=user,
        id=word_id
    )[0]

    user.pending_state = f'UPDATE_TRANSLATION:{word_id}'
    user.save()

    query.message.edit_text(text=query.message.text)

    context.bot.send_message(
        chat_id=query.message.chat_id,
        text=f'Введите новый перевод:'
    )
