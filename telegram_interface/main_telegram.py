import telebot
from telebot.apihelper import ApiTelegramException
import config


bot = telebot.TeleBot(config.bot_token)
CHAT_ID = -845538645
bot.send_message(CHAT_ID,config.template_message_pc2)



@bot.message_handler(commands=['pc1'])
def send_welcome(message):
	bot.reply_to(message, config.template_message_pc1)


@bot.message_handler(commands=['pc2'])
def send_welcome(message):
	bot.reply_to(message, config.template_message_pc1)

@bot.message_handler(commands=['rassberry'])
def send_welcome(message):
	bot.reply_to(message, config.template_message_rasp)


bot.infinity_polling()