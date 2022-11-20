import os
import config
import utils
import telebot
import time

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
    techn_interv_needed = not prediction[0]
    data_to_print = []
    i = 0
    for entry in data:
        one_line = config.rasb_features[i] + [entry]
        data_to_print.append(one_line)
        i += 1

    html = utils.get_html_from_table(data_to_print, techn_interv_needed)
    bot.reply_to(message, html, parse_mode='html')


@bot.message_handler(commands=['pc2'])
def send_welcome(message):
    """
        Sends a message when /pc2 is typed in the telegram channel
    :param message: Message written by the user to reply to
    :return: None
    """
    test = utils.Predict()
    data, prediction = test.predict_output('pc2')
    techn_interv_needed = not prediction[0]
    data_to_print = []
    i = 0
    for entry in data:
        one_line = config.rasb_features[i] + [entry]
        data_to_print.append(one_line)
        i += 1

    html = utils.get_html_from_table(data_to_print, techn_interv_needed)
    bot.reply_to(message, html, parse_mode='html')


@bot.message_handler(commands=['raspberry'])
def send_welcome(message):
    """
        Sends a message when /raspberry is typed in the telegram channel
    :param message: Message written by the user to reply to
    :return: None
    """
    test = utils.Predict()
    data, prediction = test.predict_output('raspberry')
    techn_interv_needed = prediction[0]
    data_to_print = []
    i = 0
    for entry in data:
        one_line = config.rasb_features[i] + [entry]
        data_to_print.append(one_line)
        i += 1

    html = utils.get_html_from_table(data_to_print, techn_interv_needed)
    bot.reply_to(message, html, parse_mode='html')


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
