# syntax=docker/dockerfile:1
FROM python:3.8-alpine

RUN mkdir "api"
COPY . /api

WORKDIR api

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -v -r requirements.txt

RUN rm requirements.txt

# Run Flask App
CMD["python", "app.py"]