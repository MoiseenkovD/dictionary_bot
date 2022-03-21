from telegram import InlineKeyboardMarkup, InlineKeyboardButton

get_main_word_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('Добавить слово и перевод в словарь', callback_data=f'add_word')],
        [InlineKeyboardButton('Удалить перевод и слово', callback_data=f'remove_translation')],
        [InlineKeyboardButton('Выбрать другой перевод', callback_data=f'change_translation')]
    ])