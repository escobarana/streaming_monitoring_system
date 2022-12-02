# Telegram Bot

We use a Telegram Bot in order to `alert` the user in **real-time** when one his devices is stressed, so he can act 
accordingly and also for `monitoring` so the user can freely ask the bot for the latest sensor's measurements about any 
of his devices and the bot will reply with it using a table format.

This bot is`Dockerized` and deployed in an `AWS EC2` instance being available 24/7.


## Run locally

````shell
cd telegrambot
````

````shell
pip install -r requirements.txt
````

````shell
python main_telegram.py
````


Some images from the Telegram Group:

![Telegram Bot Welcome Message](../image/bot_welcome_msg.png "Welcome Message")

![Monitoring message PC1](../image/pc1_monitoring.png "Monitoring PC1")

![Monitoring message PC2](../image/pc2_monitoring.png "Monitoring PC2")

![Monitoring message RASPBERRY PI](../image/raspb_monitoring.png "Monitoring RASPBERRY")

![Alert message PC1 + correction of prediction](../image/pc1_alert_with_correction.png "Alert PC1")
