# Data Simulator

Web application (Flask based) using Swagger for documentation purposes.

Three kafka producers (two PCs and one Raspberry Pi) that will send sensor's data every 5 seconds to three different Kafka 
topics. A consumer will subscribe to this three topics, monitoring the messages by predicting in real-time the device status
and alerting the final user if one of his devices is burning out based on the prediction of the machine learning model.
The sensor's data and the predictions will be stored in AWS DynamoDB, accessible by the user whenever he requests through 
a bot implemented using `Telegram`. This bot serves both use cases, `alerting` and `monitoring`.

The machine learning models that predicts the status of each device are deployed in AWS S3 bucket.


## Structure of the project

    ├── .github                     : CI/CD pipeline using GitHub Actions
    |  └── workflows                : Contains yaml files that trigger the workflows in GitHub Actions.
    |       ├── docker_flask.yml 
    |       ├── docker_telegram.yml 
    |       ├── terraform.yml 
    |       └── unittests.yml 
    ├── api                         : Python Flask REST API with Swagger
    |   ├── helpers
    |   ├── tests
    |   ├── .dockerignore
    |   ├── __init__.py
    |   ├── app.py
    |   ├── Dockerfile
    |   ├── README.md
    |   └── requirements.txt 
    ├── generators                   : Sensor's data generators in real-time
    |   ├── kafkaproducer
    |   ├── raspberrypi
    |   ├── sensors
    |   ├── __init__.py
    |   ├── pc.py
    |   ├── raspberry.py
    |   ├── README.md
    ├── iac                         : Infrastructure as Code 
    |   ├── .terraform
    |   ├── .gitignore
    |   ├── config.tf
    |   ├── data.tf
    |   ├── main.tf
    |   ├── outputs.tf
    |   ├── terraform.tfstate
    |   ├── terraform.tfstate.backup
    |   └── variables.tf 
    |   └── README.md               : Further explanations on IaC part
    ├── kafkaconsumer               : Kafka Consumer
    |   ├── schemas
    |   ├── __init__.py
    |   ├── config.py
    |   ├── consumer.py
    |   ├── dynamodb.py
    |   ├── main.py
    |   ├── pc.py
    |   ├── predictor.py
    |   ├── raspberry.py
    |   ├── README.md
    ├── model                        : ML Modeling
    |   ├── data
    |   ├── exported_models
    |   ├── __init__.py
    |   ├── config.py
    |   ├── data_retriever.py
    |   ├── model_pc1.py
    |   ├── model_raspberry.py
    |   ├── model_training.py
    |   ├── README.md
    ├── telegrambot                  : Telegram Bot
    |   ├── .dockerignore
    |   ├── __init__.py
    |   ├── config.py
    |   ├── Dockerfile
    |   ├── dynamodb_config.py
    |   ├── main_telegram.py
    |   ├── requirements.txt
    |   ├── utils.py
    |   ├── README.md
    ├── image                       : Folder containing all the images used in the README.md files.
    ├── .env                        : File to store environment variables (not published)
    ├── .gitignore
    ├── README.md
    ├── requirements.txt            : File containing the library requirements to run the project locally
    └── setup.py                    : Setup python file of the project

**Refer to each section `README.md` file for further details.**

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

The sensor schema can be found in `generators > kafkaproducer > raspberry_sensor_schema.py and pc_sensor_schema.py`. 
These schemas will ensure that every sensor record sent to the kafka topic will have this structure having always 
properly formatted messages.


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


## Run Flask API using Docker

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


## Run Flask API locally

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
