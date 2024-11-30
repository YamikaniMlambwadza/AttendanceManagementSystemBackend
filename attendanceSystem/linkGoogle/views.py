from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from .google_sheets import get_google_sheet_data

@csrf_exempt
def fetch_sheet_data(request):
    SHEET_ID = '1HO26E8XimkSdBGrLMom7ahqWfciWFG1tHIjs-K1FWRY'  # Your Google Sheet ID
    RANGE_NAME = 'Sheet1!A1:D10'  # The range of your sheet to read data from
    CREDENTIALS_FILE = 'Secrets/testproject-441814-b1ad929bb674.json'  
    TARGET_SHEET_ID = '15tlH22Jdhps4M5HkvFiq-ZB551Omf5y-d5uS_xmsICw'  

    try:
        if request.method == "POST":
            # Parse    incoming JSON from React Native app
            data = json.loads(request.body)
            registration_number_from_app = data.get('registration_number')

            if not registration_number_from_app:
                return JsonResponse({'error': 'Missing registration number'}, status=400)

            # Normalize input registration number to uppercase and strip spaces
            registration_number_from_app = registration_number_from_app.strip().upper()

            # Fetch data from the source Google Sheet
            data_from_sheet = get_google_sheet_data(SHEET_ID, RANGE_NAME, CREDENTIALS_FILE)
            if not data_from_sheet:
                return JsonResponse({'error': 'Failed to fetch data from Google Sheets'}, status=500)

            # Extract and normalize registration numbers from the sheet (assuming registration numbers are in the 3rd column)
            registration_numbers_from_sheet = [
                str(row[2]).strip().upper() for row in data_from_sheet[1:] if len(row) > 2
            ]

            # Check if the scanned registration number exists in the sheet
            matched_row = next(
                (row for row in data_from_sheet[1:] if len(row) > 2 and str(row[2]).strip().upper() == registration_number_from_app),
                None
            )

            if not matched_row:
                return JsonResponse({'exists': False, 'error': 'Registration number not found'}, status=404)

            # Write matched data to the target Google Sheet
            try:
                scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
                creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
                client = gspread.authorize(creds)

                # Access the target sheet and append the data (e.g., name and registration number)
                target_sheet = client.open_by_key(TARGET_SHEET_ID).sheet1  
                name = matched_row[1].strip() if len(matched_row) > 1 else "Unknown"
                target_sheet.append_row([name, registration_number_from_app])  
            except Exception as e:
                return JsonResponse({'error': f'Failed to write to target sheet: {str(e)}'}, status=500)

            return JsonResponse({'exists': True, 'name': matched_row[1].strip()})

        elif request.method == "GET":
            # Fetch the sheet data (for debugging or viewing the current sheet contents)
            data_from_sheet = get_google_sheet_data(SHEET_ID, RANGE_NAME, CREDENTIALS_FILE)
            if not data_from_sheet:
                return JsonResponse({'error': 'Failed to fetch data from Google Sheets'}, status=500)

            # Format the data from the sheet for easy viewing (optional, for debugging purposes)
            sheet_data = [
                {
                    'column1': row[0] if len(row) > 0 else None,
                    'column2': row[1] if len(row) > 1 else None,
                    'column3': row[2] if len(row) > 2 else None,
                    'column4': row[3] if len(row) > 3 else None,
                }
                for row in data_from_sheet
            ]

            return JsonResponse({'sheet_data': sheet_data})

        else:
            return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
