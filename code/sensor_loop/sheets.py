import gspread
import logging
from google.auth import exceptions as gauthExceptions
from requests import exceptions as reqExceptions

logger = logging.getLogger(__name__)

class SheetWrapper:
    def __init__(self, sheet):
        self.sheet = sheet

    def appendRow(self, row):
        logger.info('Writing row to sheet: ' + repr(row))
        try:
            self.sheet.append_row(row)
            logger.info('Success')
            return True
        except (gauthExceptions.TransportError, reqExceptions.ConnectionError, reqExceptions.ReadTimeout) as e:
            logger.critical('Connection failure when logging data')
            logger.critical(e)
            return False

def openSheet(url, worksheet, creds):
    # Create a client to interact with the Google Drive API
    gc = gspread.service_account(filename=creds)

    # Open spreadsheet
    logger.info('Authenticating and opening spreadsheet')
    sheet: gspread.models.Worksheet # declare variable and its type without assignment
    try:
        sheet = gc.open_by_url(url).worksheet(worksheet)
    except gauthExceptions.TransportError as e:
        logger.critical('Connection failure when opening spreadsheet')
        logger.critical(e)
        return False
    except gauthExceptions.GoogleAuthError as e:
        logger.critical('Authentication failure when opening spreadsheet')
        logger.critical(e)
        return False

    logger.info('Success')
    return SheetWrapper(sheet)
