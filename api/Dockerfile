# syntax=docker/dockerfile:1
FROM python:3.8-alpine

RUN mkdir "api"
COPY . /api

WORKDIR api

RUN pip install -U pip && \
    pip install --no-cache-dir -v -r requirements.txt

RUN rm requirements.txt

ENV DEVICE PC

EXPOSE 5000

# Run Flask App
CMD ["python", "app.py"]