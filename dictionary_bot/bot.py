import configs as configs
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext, CommandHandler, Updater, CallbackQueryHandler, MessageHandler, Filters
from googletrans import Translator
from django.utils import timezone as tz


import os, django

from dictionary_bot.configs import configs
from dictionary_bot.constans import SUPPORTED_LANGUAGES
from dictionary_bot.utils import get_main_word_keyboard

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


def button(update: Update, context: CallbackContext):
    query = update.callback_query

    query.answer()

    command, *payload = query.data.split(':')

    user = Users.objects.get(
        chat_id=query.message.chat_id,
    )

    if command == 'add_word':
        translator = Translator()

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
    elif command == 'remove_translation':
        query.message.reply_to_message.delete()
        query.message.delete()
    elif command == 'change_lang':
        translator = Translator()

        original_word = query.message.reply_to_message.text
        translated_original_language = translator.detect(original_word).lang

        translated_word = query.message.text
        translated_language = translator.detect(translated_word).lang

        lang_buttons = []

        for lang in SUPPORTED_LANGUAGES:
            if translated_language == lang or translated_original_language == lang:
                continue
            lang_buttons.append([InlineKeyboardButton(lang, callback_data=f'change_language:{lang}')])

        lang_buttons.append([InlineKeyboardButton('Назад', callback_data=f'to_back')])

        lang_keyboard = InlineKeyboardMarkup(lang_buttons)

        query.edit_message_text(
            text=query.message.text,
            reply_markup=lang_keyboard
        )
    elif command == 'change_translation':
        translator = Translator()

        original_word = query.message.reply_to_message.text

        lang_code = translator.detect(original_word).lang

        if lang_code == 'en':
            lang_code = 'ru'
        else:
            lang_code = 'en'

        translated_word = translator.translate(original_word, dest=lang_code).extra_data['all-translations']

        buttons = []

        for i, translation_list in enumerate(translated_word):
            translation_type = translation_list[0]
            buttons.append([InlineKeyboardButton(translation_type.title(), callback_data=f'check_translation_type:{i}')])

        buttons.append([InlineKeyboardButton('Назад', callback_data=f'to_back')])
        keyboard = InlineKeyboardMarkup(buttons)

        query.edit_message_text(
            text=query.message.text,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )
    elif command == 'check_translation_type':
        translator = Translator()

        original_word = query.message.reply_to_message.text
        print(original_word)

        lang_code = translator.detect(original_word).lang

        if lang_code == 'en':
            lang_code = 'ru'
        else:
            lang_code = 'en'

        translated_word = translator.translate(original_word, dest=lang_code).extra_data['all-translations']

        word_type_index = int(payload[0])

        buttons = []

        for i, word in enumerate(translated_word[word_type_index][1]):
            buttons.append([InlineKeyboardButton(word.title(), callback_data=f'change_translation_word:{word_type_index}:{i}')])

        buttons.append([InlineKeyboardButton('Назад', callback_data=f'to_back')])
        keyboard_words = InlineKeyboardMarkup(buttons)

        query.edit_message_text(
            text=query.message.text,
            reply_markup=keyboard_words,
        )
    elif command == 'change_translation_word':
        translator = Translator()

        original_word = query.message.reply_to_message.text

        lang_code = translator.detect(original_word).lang

        if lang_code == 'en':
            lang_code = 'ru'
        else:
            lang_code = 'en'

        translated_word = translator.translate(original_word, dest=lang_code).extra_data['all-translations']

        type_of_word = int(payload[0])

        index_of_word = int(payload[1])

        query.edit_message_text(
            text=translated_word[type_of_word][1][index_of_word],
            reply_markup=get_main_word_keyboard('')
        )
    elif command == 'change_language':
        translator = Translator()

        word = query.message.text

        lang = translator.detect(word).lang

        translated_word = translator.translate(word, dest=payload[0]).text

        query.edit_message_text(
            text=translated_word,
            reply_markup=get_main_word_keyboard('')
        )
    elif command == 'to_back':

        translator = Translator()

        word = query.message.reply_to_message.text

        lang = translator.detect(word).lang

        dest = 'ru'

        if 'ru' in lang:
            dest = 'en'
        else:
            dest = 'ru'

        translated_word = translator.translate(word, dest=dest).text

        query.edit_message_text(
            text=translated_word,
            reply_markup=get_main_word_keyboard('')
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

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text_obj.text,
        reply_markup=get_main_word_keyboard(''),
        reply_to_message_id=update.message.message_id,
    )


def main():
    start_handler = CommandHandler('start', start)
    dictionary_handler = CommandHandler('my_dictionary', my_dictionary)
    button_handler = CallbackQueryHandler(button)
    add_word_to_dict_handler = MessageHandler(Filters.text & ~Filters.command, message_dict)

    bot.dispatcher.add_handler(add_word_to_dict_handler)
    bot.dispatcher.add_handler(dictionary_handler)
    bot.dispatcher.add_handler(button_handler)
    bot.dispatcher.add_handler(start_handler)

    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
