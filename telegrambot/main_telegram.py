import os
import config
import utils
import telebot
import time

bot = telebot.TeleBot(os.environ['TELEGRAM_API_TOKEN'])


@bot.message_handler(func=lambda msg: msg.text is not None and '/' not in msg.text)
def reply(message):
    answer = message.text
    if answer.upper() == 'N':
        msg = message.reply_to_message.text
        tmp = msg.split('\n')[0]
        device = tmp.split(' ')[0]
        uuid = tmp.split(' ')[1]
        utils.update_data_dynamodb(uuid=uuid, device=device, prediction=0)
        bot.reply_to(message, f"Thank you, {message.from_user.first_name} {message.from_user.last_name}.\n"
                              f"Your contribution helps us improve the prediction for your devices.")


@bot.message_handler(commands=['pc1'])
def send_welcome(message):
    """
        Sends a message when /pc1 is typed in the telegram channel
    :param message: Message written by the user to reply to
    :return: None
    """
    data_input = []
    val = utils.get_data_dynamodb('pc1')
    for i, elt in enumerate(config.pc1_features):
        for data in val:
            if data == elt[1]:
                print(i, data, val[data])
                data_input.append(float(val[data]))

    data_to_print = []
    i = 0
    for entry in data_input:
        one_line = config.pc1_features[i] + [entry]
        data_to_print.append(one_line)
        i += 1

    html = utils.get_html_from_table(data_to_print, val['prediction'])
    bot.reply_to(message, html, parse_mode='html')


@bot.message_handler(commands=['pc2'])
def send_welcome(message):
    """
        Sends a message when /pc2 is typed in the telegram channel
    :param message: Message written by the user to reply to
    :return: None
    """
    data_input = []
    val = utils.get_data_dynamodb('pc2')
    for i, elt in enumerate(config.pc2_features):
        for data in val:
            if data == elt[1]:
                print(i, data, val[data])
                data_input.append(float(val[data]))

    data_to_print = []
    i = 0
    for entry in data_input:
        one_line = config.pc2_features[i] + [entry]
        data_to_print.append(one_line)
        i += 1

    html = utils.get_html_from_table(data_to_print, val['prediction'])
    bot.reply_to(message, html, parse_mode='html')


@bot.message_handler(commands=['raspberry'])
def send_welcome(message):
    """
        Sends a message when /raspberry is typed in the telegram channel
    :param message: Message written by the user to reply to
    :return: None
    """
    data_input = []
    val = utils.get_data_dynamodb('raspberry')
    for i, elt in enumerate(config.rasb_features):
        for data in val:
            if data == elt[1]:
                print(i, data, val[data])
                data_input.append(float(val[data]))

    data_to_print = []
    i = 0
    for entry in data_input:
        one_line = config.rasb_features[i] + [entry]
        data_to_print.append(one_line)
        i += 1

    html = utils.get_html_from_table(data_to_print, val['prediction'])
    bot.reply_to(message, html, parse_mode='html')


def main():
    """
        Main method of the file. Runs the bot with infinite polling
    :return: None
    """
    initial_text = f"Hello User!\n" \
                   f"Welcome to your Streaming Monitoring System\n" \
                   f"Type one of these options to see the latest sensor's data of one of your devices:\n" \
                   f"\t/pc1\n" \
                   f"\t/pc2\n" \
                   f"\t/raspberry\n"
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    bot.send_message(chat_id=chat_id, text=initial_text)
    try:
        # Infinite loop
        bot.infinity_polling()
    except:
        time.sleep(10)


if __name__ == '__main__':
    main()
