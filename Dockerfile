FROM python:3.9.0-slim-buster

WORKDIR /opt/app
RUN apt-get update 
RUN apt-get install -y libgpiod2

COPY ./app/sensor_loop/requirements.txt .
RUN pip install -r requirements.txt

COPY ./app/ .
ENV SHEET_URL='https://docs.google.com/spreadsheets/d/1WF35JEkQr129Cluj2MAp6fM3QjogUusoJytuiqaXZZs'
CMD ls
CMD python sensor_loop 
