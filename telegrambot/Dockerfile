# syntax=docker/dockerfile:1
FROM python:3.8

RUN mkdir "telegrambot"
COPY . /telegrambot

WORKDIR telegrambot

RUN pip install -U pip && \
    pip install --no-cache-dir -v -r requirements.txt

RUN rm requirements.txt

CMD ["python", "main_telegram.py"]