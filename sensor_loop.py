import gspread
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
		D18 = 111111
	adafruit_dht = MockAdafruitDHT()
	board = MockBoard()

SHEET_URL = 'https://docs.google.com/spreadsheets/d/1WF35JEkQr129Cluj2MAp6fM3QjogUusoJytuiqaXZZs'
SVC_ACC_CREDS = 'client_secret.json'

def waitForSysClockSync(timeout=30, threshold=15):
	print('Waiting for system clock to sync with NTP server')
	ntpReq: ntplib.NTPStats # declare variable and its type without assignment
	try:
		ntpReq = ntplib.NTPClient().request('pool.ntp.org', version=3)
	except (ntplib.NTPException, gaierror) as e:
		print('Could not connect to NTP server')
		print(e)
		return False
	currTime = ntpReq.tx_time
	for i in range(timeout):
		delta = abs(time() - currTime)
		if delta < threshold:
			print('System clock is synced with NTP server')
			return True
		else:
			print('.')
		sleep(1)

	print('System clock did not sync with NTP server within timeout')
	return False

def openSheet(url, worksheet, creds):
	# Create a client to interact with the Google Drive API
	gc = gspread.service_account(filename=creds)

	# Open spreadsheet
	print('Attempting to open spreadsheet')
	sheet: gspread.models.Worksheet # declare variable and its type without assignment
	try:
		sheet = gc.open_by_url(url).worksheet(worksheet)
	except gauthExceptions.TransportError as e:
		print('Failed to connect when opening spreadsheet:')
		print(e)
		sys.exit(1)
	except gauthExceptions.GoogleAuthError as e:
		print('Failed to authenticate when opening spreadsheet:')
		print(e)
		sys.exit(1)

	print('Successfully authenticated')
	return sheet


if not waitForSysClockSync():
	sys.exit(1)

print('[' + datetime.now().strftime('%m/%d/%Y %H:%M:%S') + '] Starting script')

# Connect to sensor
dhtDevice = adafruit_dht.DHT22(board.D18)

# Open sheet
sheet = openSheet(SHEET_URL, 'Humidity', SVC_ACC_CREDS)

# Program loop
while True:
	curr_date = datetime.now().strftime('%m/%d/%Y')
	curr_time = datetime.now().strftime('%H:%M:%S')

	print('Attempting to read from DHT22 sensor')
	humidity = dhtDevice.humidity
	temperature = dhtDevice.temperature
	print('Successfully read from DHT22 sensor')

	row = [curr_date, curr_time, humidity]
	print('Attempting to write: ' + repr(row))

	# Write data to sheet
	try:
		sheet.append_row(row)
		print('Successfully wrote')
	except (gauthExceptions.TransportError, reqExceptions.ConnectionError, reqExceptions.ReadTimeout) as e:
		print('Failed to connect when logging data:')
		print(e)

	sleep(15)
