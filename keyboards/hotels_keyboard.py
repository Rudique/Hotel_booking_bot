from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_btn1 = InlineKeyboardButton('1', callback_data='1')
inline_btn2 = InlineKeyboardButton('2', callback_data='2')
inline_btn3 = InlineKeyboardButton('3', callback_data='3')
inline_btn4 = InlineKeyboardButton('4', callback_data='4')
inline_btn5 = InlineKeyboardButton('5', callback_data='5')
num_keyboard = InlineKeyboardMarkup().add(inline_btn1, inline_btn2, inline_btn3, inline_btn4, inline_btn5,)
