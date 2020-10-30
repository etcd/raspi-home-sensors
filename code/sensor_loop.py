import gspread
import logging
import ntplib
import sys
from datetime import datetime
from google.auth import exceptions as gauthExceptions
from requests import exceptions as reqExceptions
from socket import gaierror
from time import sleep, time

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

SHEET_URL = 'https://docs.google.com/spreadsheets/d/1WF35JEkQr129Cluj2MAp6fM3QjogUusoJytuiqaXZZs'
SVC_ACC_CREDS = 'client_secret.json'

# Configure logger
logging.basicConfig(
	format='[%(asctime)s] %(levelname)s: %(message)s',
	datefmt='%Y-%m-%d %H:%M:%S',
	handlers=[
        logging.FileHandler("sensor_loop.log"),
        logging.StreamHandler()
    ],
	level=logging.INFO
	)

def waitForSysClockSync(timeout=30, threshold=15):
	logging.info('Waiting for system clock to sync with NTP server')
	ntpReq: ntplib.NTPStats # declare variable and its type without assignment
	try:
		ntpReq = ntplib.NTPClient().request('pool.ntp.org', version=3)
	except (ntplib.NTPException, gaierror) as e:
		logging.critical('Could not connect to NTP server')
		logging.critical(e)
		return False
	currTime = ntpReq.tx_time
	for i in range(timeout):
		delta = abs(time() - currTime)
		if delta < threshold:
			logging.info('Success')
			return True
		else:
			logging.info('.')
		sleep(1)

	logging.critical('System clock failed to sync with NTP server within timeout (%s seconds)', timeout)
	return False

def openSheet(url, worksheet, creds):
	# Create a client to interact with the Google Drive API
	gc = gspread.service_account(filename=creds)

	# Open spreadsheet
	logging.info('Authenticating and opening spreadsheet')
	sheet: gspread.models.Worksheet # declare variable and its type without assignment
	try:
		sheet = gc.open_by_url(url).worksheet(worksheet)
	except gauthExceptions.TransportError as e:
		logging.critical('Connection failure when opening spreadsheet')
		logging.critical(e)
		sys.exit(1)
	except gauthExceptions.GoogleAuthError as e:
		logging.critical('Authentication failure when opening spreadsheet')
		logging.critical(e)
		sys.exit(1)

	logging.info('Success')
	return sheet

logging.info('-------------------------------')
logging.info('        Starting script        ')
logging.info('-------------------------------')

if not waitForSysClockSync():
	sys.exit(1)

# Connect to sensor
dhtDevice = adafruit_dht.DHT22(board.D4)

# Open sheet
sheet = openSheet(SHEET_URL, 'Humidity', SVC_ACC_CREDS)

# Program loop
while True:
	curr_date = datetime.now().strftime('%m/%d/%Y')
	curr_time = datetime.now().strftime('%H:%M:%S')

	logging.info('Reading from DHT22 sensor')
	humidity = dhtDevice.humidity
	temperature = dhtDevice.temperature
	logging.info('Success')

	row = [curr_date, curr_time, humidity]
	logging.info('Writing data: ' + repr(row))

	# Write data to sheet
	try:
		sheet.append_row(row)
		logging.info('Success')
	except (gauthExceptions.TransportError, reqExceptions.ConnectionError, reqExceptions.ReadTimeout) as e:
		logging.critical('Connection failure when logging data')
		logging.critical(e)

	sleep(15)
