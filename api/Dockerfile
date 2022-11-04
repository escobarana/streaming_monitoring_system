# syntax=docker/dockerfile:1
FROM python:3.8

RUN mkdir "api"
COPY . /api

WORKDIR api

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc and-build-dependencies \
    && rm -rf /var/lib/apt/lists/* \
    && pip install cryptography \
    && apt-get purge -y --auto-remove gcc and-build-dependencies \
    && pip install numpy

RUN pip install -U pip && \
    pip install --no-cache-dir -v -r requirements.txt

RUN rm requirements.txt

ENV DEVICE PC

EXPOSE 5000

# Run Flask App
CMD ["python", "app.py"]