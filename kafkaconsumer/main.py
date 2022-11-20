from kafkaconsumer.consumer import KafkaConsumer

if __name__ == '__main__':
    KafkaConsumer().consume_json(topics=['pc1', 'pc2', 'raspberry'])
