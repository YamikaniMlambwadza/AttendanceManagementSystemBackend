from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

def get_google_sheet_data(sheet_id, range_name, credentials_file):
    #   Define the scope for read-only access
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # Authenticate using the credentials JSON file
    credentials = Credentials.from_service_account_file(credentials_file, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)

    # Access the sheet and get data
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    values = result.get('values', [])

    return values
