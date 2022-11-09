import os
from telegram_interface import config
from telegram_interface import utils
import telebot
import time

# TODO to be deleted !
# bot = telebot.TeleBot(config.bot_token)
# CHAT_ID = -845538645
# bot.send_message(CHAT_ID,config.template_message_pc2)

bot = telebot.TeleBot(os.environ['TELEGRAM_API_TOKEN'])


@bot.message_handler(commands=['pc1'])
def send_welcome(message):
    """
        Sends a message when /pc1 is typed in the telegram channel
    :param message: Message written by the user to reply to
    :return: None
    """
    test = utils.Predict()
    data, prediction = test.predict_output('pc1')
    msg = 'No technical intervention required' if prediction[0] else 'Technical intervention required'
    txt = config.template_message_pc1.format(var1=data[0],
                                             var2=data[1],
                                             var3=data[2],
                                             var4=data[3],
                                             var5=data[4],
                                             var6=data[5],
                                             var7=msg)
    bot.reply_to(message, txt)


@bot.message_handler(commands=['pc2'])
def send_welcome(message):
    """
        Sends a message when /pc2 is typed in the telegram channel
    :param message: Message written by the user to reply to
    :return: None
    """
    test = utils.Predict()
    data, prediction = test.predict_output('pc2')
    msg = 'No technical intervention required' if prediction[0] else 'Technical intervention required'
    txt = config.template_message_pc2.format(var1=data[0],
                                             var2=data[1],
                                             var3=data[2],
                                             var4=data[3],
                                             var5=msg)
    bot.reply_to(message, txt)


@bot.message_handler(commands=['raspberry'])
def send_welcome(message):
    """
        Sends a message when /raspberry is typed in the telegram channel
    :param message: Message written by the user to reply to
    :return: None
    """
    test = utils.Predict()
    data, prediction = test.predict_output('raspberry')
    msg = 'No technical intervention required' if prediction[0] else 'Technical intervention required'
    txt = config.template_message_rasp.format(var1=data[0],
                                              var2=data[1],
                                              var3=data[2],
                                              var4=data[3],
                                              var5=data[4],
                                              var6=data[5],
                                              var7=msg)
    bot.reply_to(message, txt)


def main():
    """
        Main method of the file. Runs the bot with infinite polling
    :return: None
    """
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    bot.send_message(chat_id=chat_id, text='The bot started!')
    try:
        # Infinite loop
        bot.infinity_polling()
    except:
        time.sleep(10)


if __name__ == '__main__':
    main()
