from numpy import var
import telebot
from telebot.apihelper import ApiTelegramException
import os
import config
import utils

#bot = telebot.TeleBot(config.bot_token)
#CHAT_ID = -845538645
#bot.send_message(CHAT_ID,config.template_message_pc2)

bot = telebot.TeleBot(f"{os.environ['TELEGRAM_TELEBOT_NUM']}:{os.environ['TELEGRAM_TELEBOT_TEXT']}")

@bot.message_handler(commands=['pc1'])
def send_welcome(message):
	bot.reply_to(message, config.template_message_pc1)


@bot.message_handler(commands=['pc2'])
def send_welcome(message):
	bot.reply_to(message, config.template_message_pc1)

@bot.message_handler(commands=['rassberry'])
def send_welcome(message):
    test = utils.PREDICT()
    data,prediction =  test.predict_output('raspberry')
    txt = config.template_message_rasp.format(var1=data[0],
                                            var2=data[1],
                                            var3=data[2],
                                            var4=data[3],
                                            var5=data[4],
                                            var6=data[5])
    bot.reply_to(message, txt)


if __name__ == '__main__':
    
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    bot.send_message(chat_id=chat_id, text='The bot started')
    bot.infinity_polling()
    

