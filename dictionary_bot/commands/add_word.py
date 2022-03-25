from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from googletrans import Translator
from django.utils import timezone as tz

from dictionary_bot.models import Users, Dictionary

translator = Translator()


def add_word(update: Update, context: CallbackContext):

    query = update.callback_query

    query.answer()

    command, *payload = query.data.split(':')

    user = Users.objects.get(
        chat_id=query.message.chat_id,
    )

    original_word = query.message.reply_to_message.text
    original_word_lang_code = translator.detect(original_word).lang

    translated_word = query.message.text
    translated_word_lang_code = translator.detect(translated_word).lang

    if 'ru' in translated_word_lang_code:
        translated_word_lang_code = 'ru'

    dictionary = Dictionary.objects.get_or_create(
        user=user,
        original_word=original_word,
        translated_word=translated_word,
        original_word_lang_code=original_word_lang_code,
        translated_word_lang_code=translated_word_lang_code,
    )[0]

    if dictionary.created_at is None:
        dictionary.created_at = tz.now()

    dictionary.updated_at = tz.now()

    dictionary.save()

    query.edit_message_text(
        text=f'<strong>{query.message.text}</strong>',
        parse_mode=ParseMode.HTML
    )
