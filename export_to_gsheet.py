import gspread
from oauth2client.service_account import ServiceAccountCredentials

def export_to_gsheet(df, spreadsheet_name, worksheet_name="Sheet1"):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    # Open spreadsheet
    sheet = client.open(spreadsheet_name)
    
    try:
        worksheet = sheet.worksheet(worksheet_name)
        sheet.del_worksheet(worksheet)
    except gspread.exceptions.WorksheetNotFound:
        pass

    worksheet = sheet.add_worksheet(title=worksheet_name, rows=str(len(df)+1), cols=str(len(df.columns)))

    # Update header
    worksheet.insert_row(df.columns.tolist(), index=1)

    # Update values
    rows = df.values.tolist()
    worksheet.insert_rows(rows, row=2)
