import configs as configs
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, Updater, CallbackQueryHandler, MessageHandler, Filters
from googletrans import Translator
import re
from django.utils import timezone as tz

import os, django

from dictionary_bot.configs import configs

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dictionary_app.settings")
django.setup()

from dictionary_bot.models import Users, Dictionary

bot = Updater(token=configs['TOKEN'], use_context=True)


def start(update: Update, context: CallbackContext):
    user = Users.objects.get_or_create(
        chat_id=update.message.chat_id,
    )[0]

    user.first_name = update.message.chat.first_name
    user.last_name = update.message.chat.last_name
    user.username = update.message.chat.username

    user.save()

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Напишите слово для перевода"
    )


def new_word(update: Update, context: CallbackContext):
    query = update.callback_query

    query.answer()

    command = query.data

    user = Users.objects.get(
        chat_id=query.message.chat_id,
    )

    if command == 'add_word':
        translator = Translator()

        original_word = query.message.reply_to_message.text
        translated_word = query.message.text

        dictionary = Dictionary.objects.get_or_create(
            user=user,
            original_word=original_word,
            original_word_lang_code=translator.detect(original_word).lang,
            translated_word=translated_word,
            translated_word_lang_code=translator.detect(translated_word).lang,
        )[0]

        if dictionary.created_at is None:
            dictionary.created_at = tz.now()

        dictionary.updated_at = tz.now()

        dictionary.save()

        query.edit_message_text(text=query.message.text)

    elif command == 'my_dict':
        user = Users.objects.get(
            chat_id=query.message.chat_id
        )

        dictionary = Dictionary.objects.filter(
            user=user,
        )


def message_dict(update: Update, context: CallbackContext):
    translator = Translator()

    word = update.message.text

    lang = translator.detect(word).lang

    dest = 'ru'

    if 'ru' in lang:
        dest = 'en'
    else:
        dest = 'ru'

    text_obj = translator.translate(word, dest=dest)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('Добавить слово и перевод в словарь', callback_data=f'add_word')]
    ])

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text_obj.text,
        reply_markup=keyboard,
        reply_to_message_id=update.message.message_id,
    )


def main():
    start_handler = CommandHandler('start', start)
    new_word_handler = CallbackQueryHandler(new_word)
    add_word_to_dict_handler = MessageHandler(Filters.text & ~Filters.command, message_dict)

    bot.dispatcher.add_handler(add_word_to_dict_handler)
    bot.dispatcher.add_handler(new_word_handler)
    bot.dispatcher.add_handler(start_handler)

    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
