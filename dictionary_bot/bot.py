import enum

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater, CallbackQueryHandler, MessageHandler, Filters

import os, django

from dictionary_bot.configs import configs

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dictionary_app.settings")
django.setup()

import dictionary_bot.commands as commands

from dictionary_bot.models import Users

bot = Updater(token=configs['TOKEN'], use_context=True)


class Commands_of_words(enum.Enum):

    to_back = 0
    add_word = 1
    change_lang = 2
    change_language = 3
    remove_translation = 4
    change_translation = 5
    check_translation_type = 6
    change_translation_word = 7


def start(update: Update, context: CallbackContext):
    commands.start(update, context)


def my_dictionary(update: Update, context: CallbackContext):
    commands.my_dictionary(update, context)


def button(update: Update, context: CallbackContext):
    query = update.callback_query

    query.answer()

    command, *payload = query.data.split(':')

    command = int(command)

    user = Users.objects.get(
        chat_id=query.message.chat_id,
    )

    if command == Commands_of_words.add_word.value:
        commands.add_word(update, context)
    elif command == Commands_of_words.remove_translation.value:
        commands.remove_translation(update, context)
    elif command == Commands_of_words.change_lang.value:
        commands.change_lang(update, context)
    elif command == Commands_of_words.change_translation.value:
        commands.change_translation(update, context)
    elif command == Commands_of_words.check_translation_type.value:
        commands.check_translation_type(update, context, payload)
    elif command == Commands_of_words.change_translation_word.value:
        commands.change_translation_word(update, context, payload)
    elif command == Commands_of_words.change_language.value:
        commands.change_language(update, context, payload)
    elif command == Commands_of_words.to_back.value:
        commands.to_back(update, context)


def add_custom_translation(update: Update, context: CallbackContext):
    commands.add_custom_translation(update, context)


def message_dict(update: Update, context: CallbackContext):
    commands.message_dict(update, context)


def main():
    start_handler = CommandHandler('start', start)
    dictionary_handler = CommandHandler('my_dictionary', my_dictionary)
    button_handler = CallbackQueryHandler(button)
    add_word_to_dict_handler = MessageHandler(Filters.text & ~Filters.command & ~Filters.reply, message_dict)
    add_reduction_dict_handler = MessageHandler(Filters.text & Filters.reply & ~Filters.command, add_custom_translation)

    bot.dispatcher.add_handler(add_reduction_dict_handler)
    bot.dispatcher.add_handler(add_word_to_dict_handler)
    bot.dispatcher.add_handler(dictionary_handler)
    bot.dispatcher.add_handler(button_handler)
    bot.dispatcher.add_handler(start_handler)

    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
