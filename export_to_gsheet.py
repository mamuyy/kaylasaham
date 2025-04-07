import json
import gspread
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

def export_to_gsheet(df, spreadsheet_name, worksheet_name="Sheet1"):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Ambil dari secrets
    creds_dict = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT_JSON"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    sheet = client.open(spreadsheet_name)

    try:
        worksheet = sheet.worksheet(worksheet_name)
        sheet.del_worksheet(worksheet)
    except gspread.exceptions.WorksheetNotFound:
        pass

    worksheet = sheet.add_worksheet(title=worksheet_name, rows=str(len(df)+1), cols=str(len(df.columns)))
    worksheet.insert_row(df.columns.tolist(), index=1)
    worksheet.insert_rows(df.values.tolist(), row=2)
