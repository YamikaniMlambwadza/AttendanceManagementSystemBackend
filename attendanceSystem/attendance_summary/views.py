import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# The Google Sheets credentials file and target sheet details
CREDENTIALS_FILE = 'Secrets/testproject-441814-b1ad929bb674.json'
TARGET_SHEET_ID = '15tlH22Jdhps4M5HkvFiq-ZB551Omf5y-d5uS_xmsICw'

def get_google_sheet_data(sheet_id, range_name, credentials_file):
    try:
        # Authorize using the credentials file
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
        client = gspread.authorize(creds)

        #         Fetch the Google Sheet data
        sheet = client.open_by_key(sheet_id)
        data = sheet.values_get(range_name)
        return data.get('values', [])

    except Exception as e:
        print(f"Error fetching data from Google Sheets: {e}")
        return None

@csrf_exempt
def fetch_attendance_summary(request):
    try:
        # Define the range where the data is written in the target Google Sheet
        RANGE_NAME = 'Sheet1!A1:E'  # Adjust as needed based on the sheet structure
        
        # Fetch data from the target sheet
        data_from_sheet = get_google_sheet_data(TARGET_SHEET_ID, RANGE_NAME, CREDENTIALS_FILE)
        
        if not data_from_sheet:
            return JsonResponse({'error': 'Failed to fetch data from Google Sheets'}, status=500)

        # Format the data for the response
        attendance_summary = [
            {
                'name': row[0] if len(row) > 0 else None,
                'registration_number': row[1] if len(row) > 1 else None
            }
            for row in data_from_sheet
        ]

        return JsonResponse({'attendance_summary': attendance_summary})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
