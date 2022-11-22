# Kafka Consumer

There is one consumer subscribes to the three topics available in our cluster, and it's deployed in AWS EC2 instance 
and running 24/7 consuming new messages as soon as there's any. 

This consumer consumes a message, then makes the machine learning prediction on this message (whether the device given
the sensor's measurement inputs is stressed or not) and writes both the message and the prediction as an item in
`AWS DynamoDB`. 

Before writing the data, the consumer checks the result of the prediction. If the prediction is `True`, meaning that the 
device is stressed, an alert is immediately sent to the user of the device letting him know about the situation of this 
device. This is achieved using a `Telegram Bot`.


## Sensor Schema (JSON) - Schema Registry

The topic schemas can be found in `schemas > raspberry_sensor_schema.py and pc_sensor_schema.py`. 
These schemas will be used for the decoding of the message when consumed.


## Run the consumer locally

This process will not stop unless you stop it manually, simply press `Ctrl + C` keys in your keyboard to make it stop.

````shell
cd kafkaconsumer
````

````shell
pip install -r requirements.txt
````

````shell
python main.py
````
