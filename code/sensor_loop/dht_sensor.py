import logging
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

logger = logging.getLogger(__name__)

class SensorWrapper:
    def __init__(self, sensor):
        self.sensor = sensor

    def read(self):
        # Read from sensor
        logger.info('Reading from DHT22 sensor')
        humidity: float
        temperature: float
        try:
            humidity = self.sensor.humidity
            temperature = self.sensor.temperature
        except RuntimeError as e:
            logger.critical('Sensor failure: DHT sensor could not be polled')
            logger.critical(e)
            return (None, None)

        logger.info('Success')
        return (humidity, temperature)

def connect():    
    # Connect to sensor
    logging.info('Connecting to DHT22 sensor')

    dhtSensor: adafruit_dht.DHT22
    try:
        dhtSensor = adafruit_dht.DHT22(board.D4)
    except RuntimeError as e:
        logging.critical('Connection failure: DHT sensor could not be found')
        logging.critical(e)
        return False

    logging.info('Success')
    return SensorWrapper(dhtSensor)
