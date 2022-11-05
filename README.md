# Data Simulator

Web application (Flask based) that will maintain one or several device's data simulator while the app is running.

Each device instance will work as an all-in-one state machine, and will send their data every few seconds to a Kafka 
topic.

The data from Kafka will be consumed by DynamoDB sink connector using Kafka Connect and also, it will be consumed by 
the Machine Learning Models to improve the predictions.

All this data will be used to monitor the health of the devices and predict whether they will fail or not. This is 
achieved thanks to the Federated Learning models developed.


## Table reference of the sensors' measure values

| Sensor Type | Measure                       |
|-------------|-------------------------------|
| Temperature | `ºC (Celsius)`                |
| Power       | `W (Watt)`                    |
| Load        | `% (percentage)`              |
| Voltage     | `V (Volt)`                    | 
| Fan         | `CFM (Cubic Feet per Minute)` | 
| Clock       | `GHz (GigaHertz)`             | 

## Sensor Schema (JSON) - Schema Registry

The sensor schema can be found in `generators > kafka > raspberry_sensor_schema.py`. This schema will ensure that every 
sensor record sent to the kafka topic will have this structure having always properly formatted messages.

## Environmental Variables

| Variable                | Description                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| `KAFKA_CLUSTER_KEY`     | Confluent Cloud Cluster Key                                                 |
| `KAFKA_CLUSTER_SECRET`  | Confluent Cloud Cluster Secret                                              |
| `KAFKA_BROKER_SETTINGS` | Confluent Cloud Cluster Endpoint                                            |
| `KAFKA_SCHEMA_ENDPOINT` | Confluent Cloud Schema Registry Endpoint                                    |
| `SCHEMA_USERNAME`       | Confluent Cloud Schema Registry Key                                         |
| `SCHEMA_PASSWORD`       | Confluent Cloud Schema Registry API Secret                                  |
| `TOPIC_NAME_IOT`        | Topic name to produce records from the Raspberry Pi to Kafka                |
| `TOPIC_NAME`            | Topic name to produce records to Kafka                                      |
| `AWS_ACCESS_KEY`        | AWS Access Key to deploy the Flask REST API to                              |
| `AWS_SECRET_ACCESS_KEY` | AWS Secret Access Key to deploy the Flask REST API to                       |
| `DOCKER_HUB_USERNAME`   | Docker Hub registry username (to build and publish docker image of the app) |
| `DOCKER_HUB_TOKEN`      | Docker Hub registry Token (to build and publish docker image of the app)    |
| `TF_CLOUD_TOKEN`        | Terraform Cloud Token to automate the deployment in AWS                     |
| `DEVICE`                | Device from where you are running the application ['RASPBERRY', 'PC']       |


## Run using Docker

Download image:

```shell
  cd api
``` 
```shell
  docker pull -t escobarana/sensorsapi:latest
```

Run image:

```shell
  docker run -p 5000:5000 -t -i escobarana/sensorsapi:latest --env-file .env
```

## Run locally

OpenHardwareMonitor software must be running before launching the instance. 
*https://openhardwaremonitor.org/*

Install prerequisites (if the `requirements.txt` installation fails see *Notes for further details):

```shell
  pip install -r requirements.txt
```
Run tests
```shell
  cd api
```
```shell
  python -m unittest tests/__init__.py
```

Run Flask REST API
```shell
  cd api
```
```shell
  python app.py
```


## *Notes
The `WMI` library only works in Windows OS, if you're running the code in any other OS use the `Raspberry Pi` 
configuration, comment this library in the `requirements.txt` file.


When working with an OS different than Windows (with `aarch64`), to install `confluent-kafka` library you might 
encounter some incompatibility errors since they do not provide prebuilt binary wheels for `aarch64`. You will need to 
compile it yourself, which requires to first build and install `librdkafka` from source. Follow this steps:

```shell
    sudo apt-get install -y libssl-dev zlib1g-dev gcc g++ make
    git clone https://github.com/edenhill/librdkafka
    cd librdkafka
    ./configure --prefix=/usr
    make
    pip install confluent-kafka
```

If after this installation you try to run the code and get the following error: `Undefined Symbol: rd_kafka_producev` 
it is most likely because you have an earlier version installed in `/usr` and the newest version you just installed is
located in `/usr/local` and it will not be picked up automatically. 
You can check it by running `sudo apt-get purge librdkafka1 librdkafka-dev`.

To solve this issue you have to remove the previous versions from the deb package:

```shell
  sudo apt-get purge librdkafka1 librdkafka-dev
```
