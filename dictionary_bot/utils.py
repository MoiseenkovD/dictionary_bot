from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_word_keyboard(change_lang_code):
    return InlineKeyboardMarkup([
            [InlineKeyboardButton('Добавить слово и перевод в словарь', callback_data=f'add_word')],
            [InlineKeyboardButton('Посмотреть другие переводы', callback_data=f'change_translation:{change_lang_code}')],
            [InlineKeyboardButton('Изменить язык перевода', callback_data=f'change_lang')],
            [InlineKeyboardButton('Удалить перевод и слово', callback_data=f'remove_translation')]
        ])
