import telebot
from telebot.apihelper import ApiTelegramException
import os

if __name__ == '__main__':
    bot = telebot.TeleBot(f"{os.environ['TELEGRAM_TELEBOT_NUM']}:{os.environ['TELEGRAM_TELEBOT_TEXT']}")

    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    bot.send_message(chat_id=chat_id, text='This is from bot')
