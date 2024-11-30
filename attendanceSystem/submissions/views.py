import json
import os
from django.http import JsonResponse
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import logging
from django.views.decorators.csrf import csrf_exempt

#  Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Google Sheets API configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1LJcHrGJUoAlsQ9CvP6ubMBmnHqZ1cfZmOuopCD7tKzA'
RANGE = 'Sheet1!A1:A'  # Update this range if necessary

# Path to service account file
SERVICE_ACCOUNT_FILE = 'Secrets/testproject-441814-b1ad929bb674.json'


@csrf_exempt
def write_on_google_sheet(request):
    if request.method == 'POST':
        try:
            # Parse the request body
            data = json.loads(request.body)
            id_to_write = data.get('id')

            if not id_to_write:
                logger.warning("No ID provided in request body.")
                return JsonResponse({'error': 'No ID provided'}, status=400)

            # Verify the service account file exists
            if not os.path.exists(SERVICE_ACCOUNT_FILE):
                logger.error("Service account file is missing.")
                return JsonResponse({'error': 'Service account file not found'}, status=500)

            # Authenticate with the Google Sheets API
            creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            service = build('sheets', 'v4', credentials=creds)
            sheet = service.spreadsheets()

            # Append the scanned ID to the Google Sheet
            result = sheet.values().append(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE,
                valueInputOption='RAW',
                body={'values': [[id_to_write]]}
            ).execute()

            logger.info(f"Successfully wrote ID to Google Sheet: {result}")
            return JsonResponse({'success': True, 'message': 'ID written to Google Sheet'})

        except json.JSONDecodeError:
            logger.error("Invalid JSON in request body.")
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
        except Exception as e:
            logger.error(f"Error writing to Google Sheet: {str(e)}")
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

    # Handle non-POST requests
    logger.warning(f"Invalid request method: {request.method}")
    return JsonResponse({'error': 'Invalid request method'}, status=405)
