from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def gen_markup_start():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Подготовленный объект", callback_data="test1"),
               InlineKeyboardButton("Выдающаяся способность", callback_data="test2"))
    return markup

def gen_markup_po():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Выдающаяся способность", callback_data="test3"))
    return markup

def gen_markup_vs():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Выдающаяся способность", callback_data="test4"))
    return markup