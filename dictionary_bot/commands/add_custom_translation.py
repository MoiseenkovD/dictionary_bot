from telegram import Update
from telegram.ext import CallbackContext

from googletrans import Translator

from dictionary_bot.models import Users, Dictionary

from django.utils import timezone as tz

translator = Translator()


def add_custom_translation(update: Update, context: CallbackContext):

    user = Users.objects.get(chat_id=update.message.chat_id)

    abbreviated_word = update.message.text
    abbreviated_lang = translator.detect(abbreviated_word).lang

    word = update.message.reply_to_message.text
    word_lang = translator.detect(word).lang

    dictionary = Dictionary.objects.get_or_create(
        user=user,
        original_word=word,
        translated_word=abbreviated_word,
        original_word_lang_code=word_lang,
        translated_word_lang_code=abbreviated_lang,
    )[0]

    if dictionary.created_at is None:
        dictionary.created_at = tz.now()

    dictionary.updated_at = tz.now()

    dictionary.save()
