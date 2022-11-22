# Sensor's data generators

We're using two laptops with Windows OS and a Raspberry Pi 4 Model B with Raspberry Pi OS.
For the Windows devices, they need to launch `OpenHardwareMonitor` software (*https://openhardwaremonitor.org/*) to be
able to read their sensor's data. For this reason, we chose not to deploy this part of the system and create a main
program that will send the sensor's data to a `Kafka Topic` every 5 seconds when launched.


## Sensor Schema (JSON) - Schema Registry

The topic schemas can be found in `generators > kafkaproducer > raspberry_sensor_schema.py and pc_sensor_schema.py`. 
These schemas will ensure that every sensor record sent to the kafka topic will have this structure having always 
properly formatted messages by encoding the message. Likewise, these schemas will be used later on for the decoding of
the message when consumed.


## Kafka Producer

We have one producer per device and one topic per device (three topics in total). As this code will be run locally, in the 
`environment variables` each one of the devices will have for the `TOPIC_NAME` variable the name of the topic that 
device is supposed to send the data to.

Also, in the `.env` file there are all the `Confluent Cloud` environment variables established for the code to run properly.


## Generate data and send message to kafka topic

### Using Windows PC

````shell
cd generators
````

````shell
python pc.py
````


### Using Raspberry Pi

````shell
cd generators
````

````shell
python raspberry.py
````
