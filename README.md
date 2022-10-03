# Data Simulator

Web application (Flask based) that will maintain one or several device's data simulator while the app is running.

Each device instance will work as an all-in-one state machine, and will send their data through MQTT every few seconds 
also, each device can be controlled by an API.

The data from MQTT Topic (Raspberry Pi device) will be consumed by kafka connect to be sent to kafka whereas the data 
produced by CPU will be directly produced to the kafka topic specified.

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

The sensor schema can be found in `helpers > sensor_schema.py`. This schema will ensure that every sensor 
record sent to the kafka topic will have this structure having always properly formatted messages.

## Docker

Create image:

```shell
docker build --platform linux/amd64 -t data-simulator .
```

Run image:

```shell
docker run --platform linux/amd64 --env-file .env -p 80:80 data-simulator
```

## Environmental Variables

| Variable                   | Description                                       |
|----------------------------|---------------------------------------------------|
| `MQTT_HOST`                | Host MQTT Broker                                  |
| `MQTT_PORT`                | Port MQTT Broker                                  |
| `MQTT_KEEP_ALIVE_INTERVAL` | Interval to keep alive the MQTT Broker connection |
| `MQTT_TOPIC`               | Topic name to send messages to                    |
| `HIVE_USERNAME`            | Username HIVE account                             |
| `HIVE_PASSWORD`            | Password HIVE account                             |
| `KAFKA_CLUSTER_KEY`        | Confluent Cloud Cluster Key                       |
| `KAFKA_CLUSTER_SECRET`     | Confluent Cloud Cluster Secret                    |
| `KAFKA_BROKER_SETTINGS`    | Confluent Cloud Cluster Endpoint                  |
| `KAFKA_SCHEMA_ENDPOINT`    | Confluent Cloud Schema Registry Endpoint          |
| `SCHEMA_USERNAME`          | Confluent Cloud Schema Registry Key               |
| `SCHEMA_PASSWORD`          | Confluent Cloud Schema Registry API Secret        |
| `TOPIC_NAME`               | Topic name to produce records to                  |


## Run locally

OpenHardwareMonitor software must be running before launching the instance. 
*https://openhardwaremonitor.org/*

Install prerequisites:

```shell
pip install -r requirements.txt
```

Run Flask
```shell
flask -app flas_app.py run -h 0.0.0.0 -p 80
```
