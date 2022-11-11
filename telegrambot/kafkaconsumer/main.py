import os

from telegrambot.kafkaconsumer.consumer import KafkaConsumer

# This main class is made for testing purposes
if __name__ == '__main__':
    topic = os.environ['TOPIC_NAME']
    KafkaConsumer().consume_json(topic_name=topic)
