import logging
import sys

logger = logging.getLogger(__name__)

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

def connectDHTSensor():    
    # Connect to sensor
    logging.info('Connecting to DHT22 sensor')
    dhtSensor: adafruit_dht.DHT22
    try:
        dhtSensor = adafruit_dht.DHT22(board.D4)
    except RuntimeError as e:
        logging.critical('Connection failure: DHT sensor could not be found')
        logging.critical(e)
        sys.exit(1)
    logging.info('Success')

    return dhtSensor
