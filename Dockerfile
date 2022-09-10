FROM python:3.9

COPY . ./datasimulator

WORKDIR /datasimulator

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -v -r requirements.txt

RUN rm requirements.txt

CMD["flask", "--app", "flask_app.py", "-h", "0.0.0.0", "-p", "80"]