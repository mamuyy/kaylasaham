import gspread
from google.oauth2.service_account import Credentials
import json
import pandas as pd
import streamlit as st

def export_to_gsheet(df: pd.DataFrame, spreadsheet_name: str, worksheet_name: str = "Sheet1"):
    # Load credential dari st.secrets
    creds_dict = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT_JSON"])
    creds = Credentials.from_service_account_info(creds_dict)
    client = gspread.authorize(creds)

    # Buka spreadsheet
    sheet = client.open(spreadsheet_name)

    try:
        worksheet = sheet.worksheet(worksheet_name)
        sheet.del_worksheet(worksheet)
    except gspread.exceptions.WorksheetNotFound:
        pass

    worksheet = sheet.add_worksheet(title=worksheet_name, rows=str(len(df)+1), cols=str(len(df.columns)))

    # Header + Data
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
