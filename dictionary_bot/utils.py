from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from dictionary_bot.bot import Commands_of_words


def get_main_word_keyboard(change_lang_code):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                '📝 Добавить слово и перевод в словарь',
                callback_data=f'{Commands_of_words.add_word.value}'
            )
        ],
        [
            InlineKeyboardButton(
                '👀 Другие значения',
                callback_data=f'{Commands_of_words.change_translation.value}:{change_lang_code}'
            ),
            InlineKeyboardButton(
                '🧐 Контекст',
                callback_data=f'{Commands_of_words.examples.value}'
            )
        ],
        [
            InlineKeyboardButton(
                '🌎 Изменить язык перевода',
                callback_data=f'{Commands_of_words.change_lang.value}'
            )
        ],
        [
            InlineKeyboardButton(
                '❌ Удалить из истории',
                callback_data=f'{Commands_of_words.remove_translation.value}'
            )
        ]
    ])
