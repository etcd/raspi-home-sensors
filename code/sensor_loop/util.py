import logging
import netifaces
import ntplib
from socket import gaierror
from time import sleep, time

WAITING_PERIOD = 0.1 # seconds between checking for sync

logger = logging.getLogger(__name__)

def getMac():
    # this function gets the mac address of the current device's default internet gateway

    # get the interface name
    interface = netifaces.gateways()['default'][netifaces.AF_INET][1]
    # get the mac of the interface
    mac = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']

    return mac

# wait for system clock to sync with fetched time from NTP server
# timeout - seconds to check for before returning False
# threshold - maximum allowable difference (in seconds) between retrieved time vs system time
def waitForSysClockSync(timeout=30, threshold=15):
    logger.info('Waiting for system clock to sync with NTP server')

    ntpReq: ntplib.NTPStats # declare variable and its type without assignment
    try:
        ntpReq = ntplib.NTPClient().request('pool.ntp.org', version=3)
    except (ntplib.NTPException, gaierror) as e:
        logger.critical('Could not connect to NTP server')
        logger.critical(e)
        return False
    currTime = ntpReq.tx_time

    # number of loops required to achieve `timeout` seconds
    loops = timeout/WAITING_PERIOD
    
    for _ in range(loops):
        delta = abs(time() - currTime)

        if delta < threshold:
            logger.debug('Success')
            return True
        else:
            logger.info('.')

        sleep(WAITING_PERIOD)

    logger.critical('System clock failed to sync with NTP server within timeout (%s seconds)', timeout)
    return False
