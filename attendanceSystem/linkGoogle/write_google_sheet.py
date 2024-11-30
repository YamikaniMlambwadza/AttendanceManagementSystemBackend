import gspread
from oauth2client.service_account import ServiceAccountCredentials

#    Set up the credentials
def authorize_google_sheets(credentials_file):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(creds)
    return client

# Write data to a Google Sheet
def write_to_google_sheet(sheet_id, row_data, credentials_file):
    try:
        client = authorize_google_sheets(credentials_file)
        sheet = client.open_by_key(sheet_id).sheet1  
        sheet.append_row(row_data)  
        return True
    except Exception as e:
        print(f"Error writing to Google Sheet: {str(e)}")
        return False
