import os
import logging
import time

from telebot import TeleBot
from keyboards import markup
from database.repository import UserTableRepository


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start_handler(message):
    logging.info("Обрабатываю команду start")
    
    if UserTableRepository.user_already_have(message.chat.id):
        bot.reply_to(message, "Вы уже зарегистрированы в системе")
    else:
        bot.reply_to(message, 
                    "Привет! Чтобы зарегистрировать тебя в системе," \
                    "мне нужен твой номер телефона.\n" \
                    "Чтобы отправить номер нажми на кнопку ниже.",
                    reply_markup=markup)


@bot.message_handler(content_types=["contact"])
def contact_handler(message):
    logging.info("Обрабатываю команду contact")
    phone_number = message.contact.phone_number
    chat_id = message.chat.id
    UserTableRepository.update_chat_id(chat_id, phone_number)
    
    bot.reply_to(message, "Вы успешно зарегистрированы в системе!")


def main():
    logging.info("Бот запущен")
    
    bot.infinity_polling(timeout=10) 


if __name__ == "__main__":
    main()
