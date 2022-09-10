# Data Simulator

Web application (Flask based) that will maintain one or several device's data simulator while the app is running.

Each device instance will work as an all-in-one state machine, and will send their data through MQT every few seconds 
also, each device can be controlled by an API.

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


## Run locally

Install prerequisites:

```shell
pip install -r requirements.txt
```

Run Flask
```shell
flask -app flas_app.py run -h 0.0.0.0 -p 80
```
