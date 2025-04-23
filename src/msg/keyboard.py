from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Ввести данные 📝')]], resize_keyboard=True, one_time_keyboard=True)
test = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='111', callback_data='test')]])
send = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить')]], resize_keyboard=True, one_time_keyboard=True)