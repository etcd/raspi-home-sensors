import argparse
import logging
import ntplib
import os
import sys
from datetime import datetime
from google.auth import exceptions as gauthExceptions
from requests import exceptions as reqExceptions
from socket import gaierror
from time import sleep

from util import waitForSysClockSync
from sheets import openSheet

try:
    import adafruit_dht
    import board
except (ImportError, NotImplementedError) as e:
    class MockAdafruitDHT:
        temperature = 999999
        humidity = 888888
        def DHT22(self, pin):
            return self
    class MockBoard:
        D4 = 111111
    adafruit_dht = MockAdafruitDHT()
    board = MockBoard()

# Configure logger
logging.basicConfig(
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ],
    level=logging.INFO
    )

if __name__ == '__main__':
    logging.info('-------------------------------')
    logging.info('        Starting script        ')
    logging.info('-------------------------------')

    # Parse arguments passed into script
    parser = argparse.ArgumentParser()
    parser.add_argument('secret', help='Absolute file path to secret used to authenticate as service account with Google Sheets.')
    parser.add_argument('sheetUrl', help='URL to Google Sheet used for storing data.')
    args = parser.parse_args()

    if not waitForSysClockSync():
        sys.exit(1)

    # Connect to sensor
    logging.info('Connecting to DHT22 sensor')
    dhtDevice: adafruit_dht.DHT22
    try:
        dhtDevice = adafruit_dht.DHT22(board.D4)
    except RuntimeError as e:
        logging.critical('Connection failure: DHT sensor could not be found')
        logging.critical(e)
        sys.exit(1)
    logging.info('Success')

    # Open sheet
    sheet = openSheet(args.sheetUrl, 'Humidity', args.secret)

    # Program loop
    while True:
        # Read from sensor
        logging.info('Reading from DHT22 sensor')
        humidity: float
        temperature: float
        try:
            humidity = dhtDevice.humidity
            temperature = dhtDevice.temperature
        except RuntimeError as e:
            logging.critical('Sensor failure: DHT sensor could not be polled')
            logging.critical(e)
            sys.exit(1)
        logging.info('Success')

        # Generate row
        curr_date = datetime.now().strftime('%m/%d/%Y')
        curr_time = datetime.now().strftime('%H:%M:%S')
        row = [curr_date, curr_time, humidity]

        # Write row to sheet
        logging.info('Writing data: ' + repr(row))
        try:
            sheet.append_row(row)
            logging.info('Success')
        except (gauthExceptions.TransportError, reqExceptions.ConnectionError, reqExceptions.ReadTimeout) as e:
            logging.critical('Connection failure when logging data')
            logging.critical(e)

        sleep(15)
