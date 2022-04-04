import enum

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CommandHandler, Updater, CallbackQueryHandler, MessageHandler, Filters

import os, django

from dictionary_bot.configs import configs

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dictionary_app.settings")
django.setup()

import dictionary_bot.commands as commands

from dictionary_bot.models import Users, Dictionary

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
    remove_word_from_dict = 8
    update_meaning = 9
    examples = 10
    choose_native_lang = 11
    choose_target_lang = 12


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
    elif command == Commands_of_words.remove_word_from_dict.value:
        commands.remove_word_from_dict(update, context)
    elif command == Commands_of_words.update_meaning.value:
        commands.update_meaning(update, context)
    elif command == Commands_of_words.examples.value:
        commands.examples(update, context, payload)
    elif command == Commands_of_words.to_back.value:
        commands.to_back(update, context)
    elif command == Commands_of_words.choose_native_lang.value:
        commands.choose_native_lang(update, context)
    elif command == Commands_of_words.choose_target_lang.value:
        commands.choose_target_lang(update, context)


def editing(update: Update, context: CallbackContext):

    user = Users.objects.get(
        chat_id=update.message.chat_id
    )

    command = update.message.text

    command, *payload = command.split('_')

    word_id = int(payload[0])

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                '🗑 Удалить',
                callback_data=f'{Commands_of_words.remove_word_from_dict.value}:{payload[0]}'
            )
        ],
        [
            InlineKeyboardButton(
                '✏️ Обновить',
                callback_data=f'{Commands_of_words.update_meaning.value}:{payload[0]}'
            )
        ]
    ])

    word = Dictionary.objects.filter(
        user=user,
        id=word_id
    )[0]

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f'{word.original_word} - {word.translated_word}',
        reply_markup=keyboard
    )


def add_custom_translation(update: Update, context: CallbackContext):
    commands.add_custom_translation(update, context)


def message_dict(update: Update, context: CallbackContext):

    user = Users.objects.get(
        chat_id=update.message.chat_id
    )

    if user.target_language is None:
        commands.choose_native_lang(update, context)
        return

    if user.pending_state is None:
        commands.message_dict(update, context)
    else:
        command, *payload = user.pending_state.split(':')

        if command == 'UPDATE_TRANSLATION':
            word_id = payload[0]
            new_translation = update.message.text
            word = Dictionary.objects.filter(
                user=user,
                id=word_id
            )[0]
            word.translated_word = new_translation
            word.save()

            user.pending_state = None
            user.save()

            context.bot.send_message(
                chat_id=update.message.chat_id,
                text=f'✅ Перевод успешно сохранен'
            )


def main():
    start_handler = CommandHandler('start', start)
    dictionary_handler = CommandHandler('my_dictionary', my_dictionary)
    button_handler = CallbackQueryHandler(button)
    add_word_to_dict_handler = MessageHandler(Filters.text & ~Filters.command & ~Filters.reply, message_dict)
    add_reduction_dict_handler = MessageHandler(Filters.text & Filters.reply & ~Filters.command, add_custom_translation)
    editing_word = MessageHandler(Filters.regex('\/edit_\d+'), editing)

    bot.dispatcher.add_handler(editing_word)
    bot.dispatcher.add_handler(add_reduction_dict_handler)
    bot.dispatcher.add_handler(add_word_to_dict_handler)
    bot.dispatcher.add_handler(dictionary_handler)
    bot.dispatcher.add_handler(button_handler)
    bot.dispatcher.add_handler(start_handler)

    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
