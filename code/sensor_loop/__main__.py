import argparse
import logging
import sys
from datetime import datetime
from google.auth import exceptions as gauthExceptions
from requests import exceptions as reqExceptions
from time import sleep

from util import waitForSysClockSync
from sheets import openSheet
from dht_sensor import connectDHTSensor


# Configure logger
logging.basicConfig(
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout),]
    )

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('-------------------------------')
    logger.info('        Starting script        ')
    logger.info('-------------------------------')

    # Parse arguments passed into script
    parser = argparse.ArgumentParser()
    parser.add_argument('secret', help='Absolute file path to secret used to authenticate as service account with Google Sheets.')
    parser.add_argument('sheetUrl', help='URL to Google Sheet used for storing data.')
    args = parser.parse_args()

    # Wait for system clock to sync via NTP
    if not waitForSysClockSync():
        sys.exit(1)

    # Connect to DHT sensor
    dhtSensor = connectDHTSensor()
    if not dhtSensor:
        sys.exit(1)

    # Open sheet
    sheet = openSheet(args.sheetUrl, 'Humidity', args.secret)
    if not sheet:
        sys.exit(1)

    # Program loop
    while True:
        # Read from sensor
        logger.info('Reading from DHT22 sensor')
        humidity: float
        temperature: float
        try:
            humidity = dhtSensor.humidity
            temperature = dhtSensor.temperature
        except RuntimeError as e:
            logger.critical('Sensor failure: DHT sensor could not be polled')
            logger.critical(e)
            sys.exit(1)
        logger.info('Success')

        # Generate row
        curr_date = datetime.now().strftime('%m/%d/%Y')
        curr_time = datetime.now().strftime('%H:%M:%S')
        row = [curr_date, curr_time, humidity]

        # Write row to sheet
        logger.info('Writing data: ' + repr(row))
        try:
            sheet.append_row(row)
            logger.info('Success')
        except (gauthExceptions.TransportError, reqExceptions.ConnectionError, reqExceptions.ReadTimeout) as e:
            logger.critical('Connection failure when logging data')
            logger.critical(e)

        sleep(15)