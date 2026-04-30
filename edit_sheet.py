import os
import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv(dotenv_path=".env")

SHEET_ID = os.getenv("SHEET_ID")
if not SHEET_ID:
    raise ValueError("Missing SHEET_ID in .env")

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

spreadsheet = client.open_by_key(SHEET_ID)
worksheet = spreadsheet.sheet1


def normalize(text):
    return str(text).strip().lower()


def color_status_cell(row_number, status):
    row_index = row_number - 1
    col_index = 5  # column F

    if normalize(status) == "rejected":
        color = {
            "red": 0.8,
            "green": 0.0,
            "blue": 0.0
        }
    elif normalize(status) == "next step":
        color = {
            "red": 0.0,
            "green": 0.7,
            "blue": 0.0
        }
    else:
        color = {
            "red": 1.0,
            "green": 1.0,
            "blue": 1.0
        }

    spreadsheet.batch_update({
        "requests": [
            {
                "repeatCell": {
                    "range": {
                        "sheetId": worksheet.id,
                        "startRowIndex": row_index,
                        "endRowIndex": row_index + 1,
                        "startColumnIndex": col_index,
                        "endColumnIndex": col_index + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": color
                        }
                    },
                    "fields": "userEnteredFormat.backgroundColor"
                }
            }
        ]
    })


def update_application_status(company, job_title, new_status):
    records = worksheet.get_all_records()

    for i, row in enumerate(records, start=2):
        sheet_company = normalize(row["COMPANY"])
        sheet_job_title = normalize(row["JOB TITLE"])

        if sheet_company == normalize(company) and sheet_job_title == normalize(job_title):
            worksheet.update_acell(f"F{i}", new_status.upper())
            color_status_cell(i, new_status)
            print(f"Updated row {i} to '{new_status.upper()}'")
            return

    print("No matching application found in spreadsheet.")