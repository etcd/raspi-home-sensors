import logging
import os
import sys
from datetime import datetime, timezone
from time import sleep
# local code
from dht_sensor import connect as connectDHT
from sheets import openSheet
from util import waitForSysClockSync

POLLING_PERIOD = 15 # seconds between consecutive polls of sensors

# Configure logger
logging.basicConfig(
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout),]
    )

logger = logging.getLogger(__name__)

# Entrypoint
if __name__ == '__main__':
    logger.info('-------------------------------------------------------------')
    logger.info('                       Starting script                       ')
    logger.info('-------------------------------------------------------------')

    # Read environment variables into variables
    secretPath = os.getenv('SECRET_PATH')
    sheetUrl = os.getenv('SHEET_URL')
    deviceName = os.getenv('DEVICE_NAME', '') # defaults to empty string

    # Wait for system clock to sync via NTP
    if not waitForSysClockSync():
        sys.exit(1)

    # Connect to DHT sensor
    dhtSensor = connectDHT()
    if not dhtSensor:
        sys.exit(1)

    # Open sheet
    sheet = openSheet(sheetUrl, 'DHT22', secretPath)
    if not sheet:
        sys.exit(1)

    # Program loop
    while True:
        # Read from sensor
        humidity, temperature = dhtSensor.read()
        if not humidity or not temperature:
            # sleep(POLLING_FREQUENCY)
            # continue
            
            # might as well restart entire sensor loop; more robust
            sys.exit(1)

        # Generate row
        curr_datetime = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        row = [curr_datetime, deviceName, humidity, temperature, ]

        # Write row to sheet
        if not sheet.appendRow(row):
            sys.exit(1)

        sleep(POLLING_PERIOD)
