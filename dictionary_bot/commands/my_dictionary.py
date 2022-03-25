from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from dictionary_bot.models import Users, Dictionary


def my_dictionary(update: Update, context: CallbackContext):
    user = Users.objects.get(
        chat_id=update.message.chat_id,
    )

    dictionary = Dictionary.objects.filter(
        user=user
    ).order_by('original_word')

    words = []

    for word in dictionary:
        original_word = word.original_word
        translated_word = word.translated_word
        words.append(f'{original_word} - {translated_word} ')

    words_str = '\n'.join(words)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f'<strong>Ваш словарь:</strong>\n{words_str}',
        parse_mode=ParseMode.HTML
    )
