

import telebot
from telebot.apihelper import ApiTelegramException

bot = telebot.TeleBot("5335139215:AAGRlCYb3QtZL6jUo73Lmos2UeuRzgbApXA")

CHAT_ID = -845538645


bot.send_message(CHAT_ID,'This is from bot')
