FROM python:3.9.0-slim-buster

WORKDIR /opt/app
RUN apt install libgpiod2

COPY ./sensor_loop/requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD python sensor_loop
