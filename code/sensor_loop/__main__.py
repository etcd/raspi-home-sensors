import argparse
import logging
import sys
from datetime import datetime
from time import sleep
# local code
import db
from dht_sensor import connect as connectDHT
from sheets import openSheet
from util import getMac, waitForSysClockSync


POLLING_FREQUENCY = 15

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

    # Parse arguments passed into script
    parser = argparse.ArgumentParser()
    parser.add_argument('secret', help='Absolute file path to secret used to authenticate as service account with Google Sheets.')
    parser.add_argument('sheetUrl', help='URL to Google Sheet used for storing data.')
    parser.add_argument('localdb', help='Absolute file path to local sqlite database.')
    args = parser.parse_args()

    # Create local db
    localdb = db.Database(args.localdb)

    # Wait for system clock to sync via NTP
    if not waitForSysClockSync():
        sys.exit(1)

    # Connect to DHT sensor
    dhtSensor = connectDHT()
    if not dhtSensor:
        sys.exit(1)

    # Open sheet
    sheet = openSheet(args.sheetUrl, 'DHT22', args.secret)
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
        curr_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row = [curr_datetime, getMac(), humidity, temperature, ]

        # Log row to local DB
        db.logDHT22(localdb, *row)

        # Write row to sheet
        if not sheet.appendRow(row):
            sys.exit(1)

        sleep(POLLING_FREQUENCY)
