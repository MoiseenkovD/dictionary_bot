from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext

from dictionary_bot.bot import Commands_of_words

from googletrans import Translator

from dictionary_bot.models import Users

translator = Translator()


def change_translation(update: Update, context: CallbackContext):

    query = update.callback_query

    query.answer()

    command, *payload = query.data.split(':')

    user = Users.objects.get(
        chat_id=query.message.chat_id
    )

    original_word = query.message.reply_to_message.text

    lang_code = translator.detect(original_word).lang

    # if lang_code == 'en':
    #     lang_code = 'ru'
    # else:
    #     lang_code = 'en'

    if lang_code == user.native_language:
        lang_code = user.target_language
    else:
        lang_code = user.native_language

    try:
        translated_word = translator.translate(original_word, dest=lang_code).extra_data['all-translations']

        buttons = []

        for i, translation_list in enumerate(translated_word):
            translation_type = translation_list[0]
            buttons.append([InlineKeyboardButton(translation_type.title(), callback_data=f'{Commands_of_words.check_translation_type.value}:{i}')])

        buttons.append([InlineKeyboardButton('⬅️ Назад', callback_data=f'{Commands_of_words.to_back.value}')])
        keyboard = InlineKeyboardMarkup(buttons)

        query.edit_message_text(
            text=query.message.text,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )
    except:
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text='Слов не найдено'
        )