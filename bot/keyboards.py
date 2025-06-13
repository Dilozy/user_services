from telebot import types


markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
button = types.KeyboardButton("Поделиться телефоном", request_contact=True)
markup.add(button)