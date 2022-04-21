from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_btn1 = InlineKeyboardButton('Да', callback_data='Yes')
inline_btn2 = InlineKeyboardButton('Нет', callback_data='No')

photo_keyboard = InlineKeyboardMarkup().add(inline_btn1, inline_btn2)
