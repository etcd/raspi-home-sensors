import logging
import ntplib
from socket import gaierror
from time import sleep, time

logger = logging.getLogger(__name__)

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
    for i in range(timeout):
        delta = abs(time() - currTime)
        if delta < threshold:
            logger.info('Success')
            return True
        else:
            logger.info('.')
        sleep(1)

    logger.critical('System clock failed to sync with NTP server within timeout (%s seconds)', timeout)
    return False