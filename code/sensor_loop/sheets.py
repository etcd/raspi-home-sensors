import gspread
import logging
import sys
from google.auth import exceptions as gauthExceptions

logger = logging.getLogger(__name__)

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
        sys.exit(1)
    except gauthExceptions.GoogleAuthError as e:
        logger.critical('Authentication failure when opening spreadsheet')
        logger.critical(e)
        sys.exit(1)

    logger.info('Success')
    return sheet
