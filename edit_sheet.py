import gspread
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv

# AUTHENTICATION
scopes = ["https://www.googleapis.com/auth/spreadsheets"]

creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

# OPEN SHEET
load_dotenv(dotenv_path=".env")

sheet_id = os.getenv("SHEET_ID")
# print("sheet_id:", repr(sheet_id))


spreadsheet = client.open_by_key(sheet_id)
worksheet = spreadsheet.sheet1


def normalize(text):
    return str(text).strip().lower()


def color_status_cell(row_number, status):
    # Google Sheets API uses 0-based indexes
    row_index = row_number - 1
    col_index = 5   # column F = STATUS, zero-based is 5

    if normalize(status) == "rejected":
            color = {
            "red": 0.85,
            "green": 0.08,
            "blue": 0.08
        }
    elif normalize(status) == "next step":
            color = {
            "red": 0.08,
            "green": 0.75,
            "blue": 0.08
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

    for i, row in enumerate(records, start=2):  # row 1 is headers
        sheet_company = normalize(row["COMPANY"])
        sheet_job_title = normalize(row["JOB TITLE"])

        if sheet_company == normalize(company) and sheet_job_title == normalize(job_title):
            # Update dropdown/text value in STATUS column (F)
            worksheet.update_acell(f"F{i}", new_status.upper())

            # Color that same cell
            color_status_cell(i, new_status)

            print(f"Updated row {i} to '{new_status}' and changed color.")
            return

    print("No matching application found.")


# TEST EXAMPLE
update_application_status(
    "TESLA",
    "Intern",
    "Rejected"
)