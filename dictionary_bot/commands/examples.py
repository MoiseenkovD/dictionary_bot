from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from dictionary_bot.bot import Commands_of_words

from googletrans import Translator

from dictionary_bot.models import Users

translator = Translator()


def examples(update: Update, context: CallbackContext, payload):
    query = update.callback_query

    query.answer()

    command, *payload = query.data.split(':')

    user = Users.objects.get(
        chat_id=query.message.chat_id
    )

    word = query.message.text.lower()

    lang_code = translator.detect(word).lang

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                '📝 Добавить слово и перевод в словарь',
                callback_data=f'{Commands_of_words.add_word.value}'
            )
        ]])

    if lang_code != user.target_language:
        word = query.message.reply_to_message.text.lower()
        lang_code = translator.detect(word).lang

    # if lang_code == 'en':
    #     lang_code = 'ru'
    # else:
    #     lang_code = 'en'

    examples_of_words = []

    try:
        data = translator.translate(word, dest=lang_code).extra_data['examples']

        for examples in data:
            for example in examples:
                replace_v1 = example[0].replace("<b>", "")
                replace_v2 = replace_v1.replace("</b>", "")

                examples_of_words.append(f'📌 {replace_v2}.\n')

            examples_list_str = '\n'.join(examples_of_words)

            context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f'Примеры:\n\n'
                     f'{examples_list_str}'
            )
    except:
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text='Примеров не найдено'
        )

