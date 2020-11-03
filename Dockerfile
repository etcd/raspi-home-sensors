FROM python:3.9.0-slim-buster

WORKDIR /opt/app
RUN apt-get update 
RUN apt-get install -y libgpiod2

COPY ./app/sensor_loop/requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD python sensor_loop
